from PyQt6.QtWidgets import (
    QGraphicsProxyWidget,
    QGraphicsScene,
    QGraphicsView,
)


class RotatableContainer(QGraphicsView):
    def __init__(self, parent, widget, angle):
        super().__init__(parent)

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(widget)
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        self.proxy.setRotation(angle)
        scene.addItem(self.proxy)

    def rotate(self, angle):
        self.proxy.setRotation(angle)
