import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root
    anchors.centerIn: parent
    width: 450
    height: 550
    modal: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    background: Rectangle {
        radius: 20
        color: "white"
    }

    property var categories: []
    signal addDish(var dish)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        Label {
            text: "添加菜品"
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        // Name
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "菜品名称 *" }

            TextField {
                id: nameField
                Layout.fillWidth: true
                placeholderText: "请输入菜品名称"
                implicitHeight: 44
            }
        }

        // Category
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "分类 *" }

            ComboBox {
                id: categoryCombo
                Layout.fillWidth: true
                implicitHeight: 44
                model: categories
                textRole: "name"
            }
        }

        // Difficulty
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "难度等级" }

            RowLayout {
                Layout.fillWidth: true

                Repeater {
                    model: [1, 2, 3, 4, 5]

                    Button {
                        text: "⭐"
                        implicitWidth: 50
                        implicitHeight: 40

                        background: Rectangle {
                            radius: 8
                            color: difficultyModel.selected === modelData ? "#FDE7D3" : "#F0F0F0"
                        }

                        contentItem: Text {
                            text: parent.text.repeat(modelData)
                            color: difficultyModel.selected === modelData ? "#E3833D" : "#888"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: difficultyModel.selected = modelData
                        }
                    }
                }
            }
        }

        // Remark
        ColumnLayout {
            spacing: 8
            Layout.fillWidth: true

            Label { text: "备注" }

            TextField {
                id: remarkField
                Layout.fillWidth: true
                placeholderText: "可选备注"
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
                        showToast("请输入菜品名称")
                        return
                    }
                    var dish = {
                        name: nameField.text,
                        category_id: categoryCombo.currentIndex >= 0 ? categories[categoryCombo.currentIndex].id : 1,
                        difficulty: difficultyModel.selected || 1,
                        remark: remarkField.text,
                        enabled: true
                    }
                    addDish(dish)
                    root.close()
                }
            }
        }
    }

    // Difficulty state
    QtObject {
        id: difficultyModel
        property int selected: 1
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