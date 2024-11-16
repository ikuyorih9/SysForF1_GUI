Navigation = []

def imprimeTracking():
    if Navigation:
        print("Imprimindo navegação...")
        for item in Navigation:
            print("- ",item.title())
    else:
        print("Não ná nada na navegação.")

def push(window):
    Navigation.append(window)

def pop():
    if Navigation:
        return Navigation.pop()
    else:
        return None

def go_back(current_window):
    current_window.destroy()
    if Navigation:
        window = pop()
        if not window.winfo_viewable():
            window.deiconify()

def go_forward(current_window, function_next_window):
    push(current_window)
    imprimeTracking()
    if current_window.winfo_viewable():
        current_window.withdraw()
        current_window.quit()
    function_next_window()

def close_all_windows(current_window):
    print("Fechando todas as janelas:")
    current_window.destroy()
    while Navigation:
        window = pop()
        print("\t-", window.title())
        window.destroy()