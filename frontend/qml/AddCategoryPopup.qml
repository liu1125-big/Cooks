import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root
    anchors.centerIn: parent
    width: 400
    height: 350
    modal: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    background: Rectangle {
        radius: 20
        color: "white"
    }

    signal addCategory(var category)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        Label {
            text: "添加分类"
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        // Name
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "分类名称 *" }

            TextField {
                id: nameField
                Layout.fillWidth: true
                placeholderText: "请输入分类名称"
                implicitHeight: 44
            }
        }

        // Sort
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "排序权重" }

            TextField {
                id: sortField
                Layout.fillWidth: true
                placeholderText: "数字越小越靠前"
                implicitHeight: 44
            }
        }

        Item { Layout.fillHeight: true }

        // Buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Button {
                Layout.fillWidth: true
                text: "取消"
                implicitHeight: 50

                background: Rectangle {
                    radius: 25
                    color: "#F0F0F0"
                }

                contentItem: Text {
                    text: parent.text
                    color: "#666"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: root.close()
            }

            Button {
                Layout.fillWidth: true
                text: "添加"
                implicitHeight: 50

                background: Rectangle {
                    radius: 25
                    color: "#E3833D"
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    if (!nameField.text) {
                        showToast("请输入分类名称")
                        return
                    }
                    var category = {
                        name: nameField.text,
                        sort: parseInt(sortField.text) || 0,
                        enabled: true
                    }
                    addCategory(category)
                    root.close()
                }
            }
        }
    }

    // Toast
    function showToast(msg) {
        toastLabel.text = msg
        toastTimer.running = true
        toastPopup.open()
    }

    Rectangle {
        id: toastPopup
        anchors.centerIn: parent
        width: 200
        height: 50
        radius: 12
        color: "#80000000"

        Label {
            id: toastLabel
            anchors.centerIn: parent
            color: "white"
            font.pixelSize: 14
        }

        Timer {
            id: toastTimer
            interval: 2000
            onTriggered: toastPopup.close()
        }
    }
}