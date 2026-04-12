import streamlit as st
import os

primer3 = None
try:
    from Bio.Seq import Seq
    from Bio.SeqUtils import gc_fraction, MeltingTemp as mt
except ImportError:
    # If biopython is not available, we can implement simple functions
    def gc_fraction(seq):
        if not seq:
            return 0
        gc_count = seq.upper().count('G') + seq.upper().count('C')
        return gc_count / len(seq)

    def mt(seq):
        # Wallace rule for Tm calculation (simple approximation)
        seq = seq.upper()
        a = seq.count('A')
        t = seq.count('T')
        g = seq.count('G')
        c = seq.count('C')
        return 2 * (a + t) + 4 * (g + c)

    def translate(seq):
        # A very simplified translation table (Standard Genetic Code)
        # This is just a fallback if biopython is not available
        gencode = {
            'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
            'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
            'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
            'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
            'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
            'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
            'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
            'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
            'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
            'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
        }
        protein = ""
        for i in range(0, len(seq) - (len(seq) % 3), 3):
            codon = seq[i:i+3].upper()
            protein += gencode.get(codon, '?')
        return protein

try:
    import primer3
except ImportError:
    primer3 = None


def calc_tm(seq):
    """Return primer melting temperature with graceful fallback."""
    try:
        return mt.Tm_NN(seq)
    except AttributeError:
        return mt(seq)
    except Exception:
        return mt(seq)


def longest_homopolymer(seq):
    longest = 1
    current = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def gc_clamp_ok(seq):
    tail = seq[-5:]
    gc_in_tail = sum(base in "GC" for base in tail)
    return 1 <= gc_in_tail <= 3 and seq[-1] in "GC"


def complement(seq):
    table = str.maketrans("ATGCatgc", "TACGtacg")
    return seq.translate(table)


def reverse_complement(seq):
    return complement(seq)[::-1]


def max_3prime_complementarity(seq1, seq2, window=8):
    """Approximate 3' complementarity risk without relying on primer3 extras."""
    rc2 = reverse_complement(seq2)
    max_match = 0
    max_window = min(window, len(seq1), len(rc2))
    for size in range(1, max_window + 1):
        if seq1[-size:] == rc2[:size]:
            max_match = size
    return max_match


def evaluate_primer(seq, hairpin_value):
    gc_pct = gc_fraction(seq) * 100
    tm_val = calc_tm(seq)
    issues = []

    if not (18 <= len(seq) <= 25):
        issues.append("长度超出推荐范围")
    if not (40 <= gc_pct <= 60):
        issues.append("GC 含量不理想")
    if not (58 <= tm_val <= 64):
        issues.append("Tm 偏离推荐范围")
    if longest_homopolymer(seq) > 4:
        issues.append("存在较长同聚物")
    if not gc_clamp_ok(seq):
        issues.append("3' GC clamp 不理想")
    if hairpin_value >= 40:
        issues.append("可能存在发夹结构")

    penalty = (
        abs(tm_val - 60) * 2
        + abs(gc_pct - 50) * 0.4
        + max(0, longest_homopolymer(seq) - 3) * 6
        + (0 if gc_clamp_ok(seq) else 6)
        + max(0, hairpin_value - 24) * 0.4
    )
    return {
        "sequence": seq,
        "length": len(seq),
        "tm": tm_val,
        "gc_pct": gc_pct,
        "hairpin_th": hairpin_value,
        "issues": issues,
        "penalty": penalty,
    }


def summarize_pair(pair):
    penalties = pair["left"]["penalty"] + pair["right"]["penalty"]
    penalties += abs(pair["left"]["tm"] - pair["right"]["tm"]) * 3
    penalties += max(0, pair["heterodimer_th"] - 24) * 0.5
    penalties += max(0, pair["compl_any_th"] - 24) * 0.25
    penalties += max(0, pair["compl_end_th"] - 12) * 1.2
    penalties += max(0, pair["three_prime_match"] - 3) * 10
    penalties += abs(pair["product_size"] - pair["target_product_size"]) * 0.03
    return penalties


def design_primers_with_ranking(dna_seq):
    if primer3 is None:
        raise RuntimeError("未安装 primer3-py，当前环境无法设计引物。")

    seq_len = len(dna_seq)
    min_product = max(80, min(120, seq_len // 4))
    max_product = min(seq_len - 30, 400)
    if max_product <= min_product:
        min_product = max(60, seq_len // 3)
        max_product = min(seq_len - 30, max(min_product + 20, seq_len - 30))
    target_product_size = min(max(180, min_product), max_product)

    seq_args = {
        'SEQUENCE_ID': 'DNA_Seq',
        'SEQUENCE_TEMPLATE': dna_seq,
    }

    global_args = {
        'PRIMER_TASK': 'generic',
        'PRIMER_PICK_LEFT_PRIMER': 1,
        'PRIMER_PICK_RIGHT_PRIMER': 1,
        'PRIMER_PICK_INTERNAL_OLIGO': 0,
        'PRIMER_OPT_SIZE': 20,
        'PRIMER_MIN_SIZE': 18,
        'PRIMER_MAX_SIZE': 24,
        'PRIMER_OPT_TM': 60.0,
        'PRIMER_MIN_TM': 58.0,
        'PRIMER_MAX_TM': 63.0,
        'PRIMER_PAIR_MAX_DIFF_TM': 1.5,
        'PRIMER_MIN_GC': 40.0,
        'PRIMER_MAX_GC': 60.0,
        'PRIMER_MAX_POLY_X': 4,
        'PRIMER_GC_CLAMP': 1,
        'PRIMER_MAX_END_GC': 3,
        'PRIMER_MAX_SELF_ANY_TH': 30.0,
        'PRIMER_MAX_SELF_END_TH': 12.0,
        'PRIMER_PAIR_MAX_COMPL_ANY_TH': 30.0,
        'PRIMER_PAIR_MAX_COMPL_END_TH': 12.0,
        'PRIMER_MAX_HAIRPIN_TH': 30.0,
        'PRIMER_NUM_RETURN': 5,
        'PRIMER_PICK_ANYWAY': 0,
        'PRIMER_PRODUCT_SIZE_RANGE': [[min_product, max_product]],
        'PRIMER_PRODUCT_OPT_SIZE': target_product_size,
    }

    try:
        p3_path = os.path.dirname(primer3.__file__)
        thermo_path = os.path.join(p3_path, 'src', 'libprimer3', 'primer3_config')
        if os.path.exists(thermo_path):
            global_args['PRIMER_THERMODYNAMIC_PARAMETERS_PATH'] = thermo_path + '/'
    except Exception:
        pass

    results = primer3.bindings.design_primers(seq_args, global_args)
    pair_count = results.get('PRIMER_PAIR_NUM_RETURNED', 0)
    ranked_pairs = []

    for idx in range(pair_count):
        left_seq = results.get(f'PRIMER_LEFT_{idx}_SEQUENCE')
        right_seq = results.get(f'PRIMER_RIGHT_{idx}_SEQUENCE')
        if not left_seq or not right_seq:
            continue

        left = evaluate_primer(left_seq, results.get(f'PRIMER_LEFT_{idx}_HAIRPIN_TH', 0))
        right = evaluate_primer(right_seq, results.get(f'PRIMER_RIGHT_{idx}_HAIRPIN_TH', 0))
        heterodimer_th = results.get(f'PRIMER_PAIR_{idx}_COMPL_ANY_TH', 0)
        compl_end_th = results.get(f'PRIMER_PAIR_{idx}_COMPL_END_TH', 0)
        three_prime_match = max_3prime_complementarity(left_seq, right_seq)

        pair = {
            "index": idx,
            "left": left,
            "right": right,
            "product_size": results.get(f'PRIMER_PAIR_{idx}_PRODUCT_SIZE'),
            "heterodimer_th": heterodimer_th,
            "compl_any_th": heterodimer_th,
            "compl_end_th": compl_end_th,
            "three_prime_match": three_prime_match,
            "target_product_size": target_product_size,
        }
        pair["score"] = summarize_pair(pair)
        ranked_pairs.append(pair)

    ranked_pairs.sort(key=lambda item: item["score"])
    return ranked_pairs, results, {
        "min_product": min_product,
        "max_product": max_product,
        "target_product_size": target_product_size,
    }


def render_primer_details(title, primer_info):
    st.info(f"**{title}**")
    st.write(f"序列: `{primer_info['sequence']}`")
    st.write(f"长度: {primer_info['length']} bp")
    st.write(f"Tm 值: {primer_info['tm']:.2f} °C")
    st.write(f"GC 含量: {primer_info['gc_pct']:.2f}%")
    st.write(f"发夹结构分数 (TH): {primer_info['hairpin_th']:.2f}")
    if primer_info["issues"]:
        st.warning("；".join(primer_info["issues"]))
    else:
        st.success("✅ 满足常规 PCR 引物设计建议")

st.set_page_config(page_title="DNA 序列分析器", page_icon="🧬")

# 侧边栏
st.sidebar.title("🧬 DNA 工具箱")
st.sidebar.info("这是一个简单的 DNA 序列分析工具，可以计算长度、GC 含量并翻译为蛋白质。")

# 主页面
st.title("DNA 序列分析器")
st.write("请输入您的 DNA 序列进行分析。")

# 文本输入框
dna_input = st.text_area("输入 DNA 序列:", height=200, placeholder="例如: ATGCATGC...")

# 清洗序列：移除空格、换行符等
dna_seq = "".join(dna_input.split()).upper()

if dna_seq:
    # 验证序列合法性 (简单检查是否只包含 ATGC)
    valid_bases = set("ATGC")
    if not all(base in valid_bases for base in dna_seq):
        st.warning("警告: 序列中包含非 ATGC 碱基。")

    st.divider()
    
    # 1. 长度
    length = len(dna_seq)
    
    # 2. GC 含量
    try:
        # If biopython is used
        gc_val = gc_fraction(dna_seq) * 100
    except:
        # Fallback
        gc_val = gc_fraction(dna_seq) * 100
    
    # 3. 翻译
    try:
        # If biopython is used
        if 'Seq' in globals():
            protein_seq = str(Seq(dna_seq).translate())
        else:
            protein_seq = translate(dna_seq)
    except Exception as e:
        protein_seq = f"翻译失败: {str(e)}"

    # 显示结果
    col1, col2 = st.columns(2)
    with col1:
        st.metric("序列长度", f"{length} bp")
    with col2:
        st.metric("GC 含量", f"{gc_val:.2f}%")

    st.subheader("蛋白质序列")
    st.code(protein_seq, language="text")

    st.divider()
    st.subheader("引物设计")
    if st.button("🧬 设计引物"):
        if len(dna_seq) < 50:
            st.error("序列太短，无法设计引物（建议至少 50 bp）。")
        else:
            with st.spinner("正在使用 Primer3 设计引物..."):
                try:
                    ranked_pairs, results, design_window = design_primers_with_ranking(dna_seq)

                    st.caption(
                        f"设计窗口: 产物 {design_window['min_product']}-{design_window['max_product']} bp，"
                        f"目标产物长度 {design_window['target_product_size']} bp。"
                    )

                    if ranked_pairs:
                        best_pair = ranked_pairs[0]
                        col1, col2 = st.columns(2)

                        with col1:
                            render_primer_details("正向引物 (Forward)", best_pair["left"])

                        with col2:
                            render_primer_details("反向引物 (Reverse)", best_pair["right"])

                        st.success(
                            f"推荐引物对产物大小: {best_pair['product_size']} bp；"
                            f"Tm 差值: {abs(best_pair['left']['tm'] - best_pair['right']['tm']):.2f} °C。"
                        )

                        st.write(
                            f"引物对互补风险: ANY_TH={best_pair['compl_any_th']:.2f}，"
                            f"END_TH={best_pair['compl_end_th']:.2f}，"
                            f"3' 末端连续互补={best_pair['three_prime_match']} bp。"
                        )

                        if len(ranked_pairs) > 1:
                            st.subheader("更多候选引物对")
                            summary_rows = []
                            for pair in ranked_pairs:
                                summary_rows.append({
                                    "候选": f"Pair {pair['index'] + 1}",
                                    "产物长度(bp)": pair["product_size"],
                                    "Forward": pair["left"]["sequence"],
                                    "Reverse": pair["right"]["sequence"],
                                    "Tm差值(°C)": round(abs(pair["left"]["tm"] - pair["right"]["tm"]), 2),
                                    "评分": round(pair["score"], 2),
                                })
                            st.dataframe(summary_rows, use_container_width=True)
                    else:
                        st.error("无法找到满足所有约束条件的引物对。请尝试调整序列或放宽限制。")
                        if 'PRIMER_LEFT_EXPLAIN' in results:
                            st.write("诊断信息:", results['PRIMER_LEFT_EXPLAIN'])
                            st.write(results.get('PRIMER_RIGHT_EXPLAIN', ''))
                            st.write(results.get('PRIMER_PAIR_EXPLAIN', ''))

                except Exception as e:
                    st.error(f"引物设计出错: {str(e)}")

else:
    st.info("请输入 DNA 序列以开始分析。")
