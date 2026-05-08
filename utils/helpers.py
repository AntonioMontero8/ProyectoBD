def limpiar_ventana(ventana):
    # 1. Eliminar todos los widgets
    for widget in ventana.winfo_children():
        widget.destroy()
    
    # 2. Resetear la configuración de columnas (hasta un rango razonable, ej. 50)
    for i in range(10):
        ventana.grid_columnconfigure(i, weight=0)
        ventana.grid_rowconfigure(i, weight=0)
