import copy
import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicheAlbum1 = None
        self._choicheAlbum2 = None

    def handleCreaGrafo(self, e):
        try:
            n = int(self._view._txtNumCanzoni.value)
        except ValueError:
            self._view.create_alert("Inserire un numero intero")
            return

        self._model.buildGraph(n)
        nN, nE = self._model.getGraphSize()

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))

        album = self._model.nodes
        for a in album:
            self._view._ddAlbum1.options.append(ft.dropdown.Option(data=a, text= a.Title, on_click=self.getSelectedAlbum1))
            self._view._ddAlbum2.options.append(ft.dropdown.Option(data=a, text=a.Title, on_click=self.getSelectedAlbum2))
        self._view.update_page()

    def getSelectedAlbum1(self, e):
        if e.control.data is None:
            self._choicheAlbum1 = None
        else:
            self._choicheAlbum1 = e.control.data

    def getSelectedAlbum2(self, e):
        if e.control.data is None:
            self._choicheAlbum2 = None
        else:
            self._choicheAlbum2 = e.control.data

    def handleAdiacenze(self, e):
        if self._choicheAlbum1 is None:
            self._view.create_alert("Selezionare un album")
            return
        v0 = self._choicheAlbum1
        successori = self._model.getSuccessori(v0)
        adiacenze = []
        for n in successori:
            adiacenze.append((n, self._model.getAdia(n)))

        adiacenze = sorted(adiacenze, key=lambda x: x[1], reverse=True)
        self._view.txt_result.clean()
        for nodo in adiacenze:
            self._view.txt_result.controls.append(ft.Text(f"{nodo[0].Title}, bilancio = {nodo[1]}"))
        self._view.update_page()

    def handlePath(self, e):
        if self._choicheAlbum1 is None:
            self._view.create_alert("Selezionare un album 1")
            return
        else:
            v0 = self._choicheAlbum1

        if self._choicheAlbum2 is None:
            self._view.create_alert("Selezionare un album 2")
            return
        else:
            vFine = self._choicheAlbum2

        try:
            soglia = int(self._view._txtInSoglia.value)
        except ValueError:
            self._view.create_alert("Inserire un valore intero")

        bestPath = self._model.getBestPath(v0, soglia, vFine)

        self._view.txt_result.clean()
        for i in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{i.Title}"))

        self._view.update_page()

