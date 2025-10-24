import xlwings as xw

# Abre o Excel diretamente e mantém visível
wb = xw.Book("hello_world.xlsm")  # ou use xw.Book.caller() se estiver usando RunPython
wb.app.visible = True  # Deixa o Excel visível

sheet = wb.sheets[0]
sheet.range("A1").value = "Olá, Amraga! Python + Excel funcionando!"
print("Script executado com sucesso!")

wb.save()
# Não fecha o Excel para você poder ver
# wb.close()  # apenas se quiser fechar
