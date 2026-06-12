import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    color: "#80000000"
    anchors.fill: parent
    z: -1

    MouseArea {
        anchors.fill: parent
        onClicked: parent.parent.focus = true
    }
}