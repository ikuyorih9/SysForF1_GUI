Navigation = []

def imprimeTracking():
    if Navigation:
        print("Imprimindo navegação...")
        for item in Navigation:
            print("- ",item.title())
    else:
        print("Não ná nada na navegação.")

def push(window):
    print(f"Pushing {window.title()} na navegação...")
    Navigation.append(window)

def pop():
    print(f"Popping {Navigation[-1].title()} na navegação...")
    return Navigation.pop()

def go_back(current_window):
    current_window.destroy()
    window = pop()
    print(window.title())
    if not window.winfo_viewable():
        window.deiconify()