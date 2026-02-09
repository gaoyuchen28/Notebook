try:
    import mathematics  # Incorrect module name
    print(mathematics.pi)
except ImportError:
    print("Module not found! Please check the module name or install it if necessary.")