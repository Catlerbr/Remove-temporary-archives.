import ctypes
import os
import shutil
import sys
import tempfile


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False


def clear_folder(path: str) -> tuple[int, int]:
    """Remove o conteudo de uma pasta, sem apagar a pasta em si.
    Retorna (itens removidos, itens com erro)."""
    removed = 0
    errors = 0

    if not os.path.isdir(path):
        print(f"  Pasta nao encontrada: {path}")
        return removed, errors

    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        try:
            if os.path.isdir(full_path) and not os.path.islink(full_path):
                shutil.rmtree(full_path, ignore_errors=False)
            else:
                os.remove(full_path)
            removed += 1
        except OSError:
            # Arquivos em uso pelo sistema ou por programas sao ignorados
            errors += 1

    return removed, errors


def main() -> None:
    if not is_admin():
        print("Este script precisa ser executado como Administrador.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    targets = [
        ("Prefetch", r"C:\Windows\Prefetch"),
        ("Temp do sistema", r"C:\Windows\Temp"),
        ("Temp do usuario", tempfile.gettempdir()),
    ]

    total_removed = 0
    total_errors = 0

    for i, (label, path) in enumerate(targets, start=1):
        print(f"[{i}/{len(targets)}] Limpando {label} ({path})...")
        removed, errors = clear_folder(path)
        total_removed += removed
        total_errors += errors
        print(f"  Removidos: {removed} | Ignorados (em uso): {errors}")

    print()
    print(f"Limpeza concluida. Total removido: {total_removed}. Ignorados: {total_errors}.")
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()