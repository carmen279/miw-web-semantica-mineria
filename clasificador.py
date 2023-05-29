import fasttext

clasificador = fasttext.train_supervised("training.txt", epoch=30)
resultados = clasificador.test("test.txt")
clasificador.save_model("clasificador.bin")

print("Results: " + str(resultados))
print("Test Accuracy: " + str(resultados[1]))