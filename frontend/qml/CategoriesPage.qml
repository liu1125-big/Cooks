import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property var categoryList: []
    property var apiService: null
    signal refresh()
    signal deleteCategory(var categoryId)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        // Header
        RowLayout {
            Layout.fillWidth: true

            Label {
                text: "分类管理"
                font.pixelSize: 36
                font.bold: true
            }

            Item { Layout.fillWidth: true }

            Button {
                text: "刷新"
                implicitWidth: 80
                implicitHeight: 36

                background: Rectangle {
                    radius: 18
                    color: "#F0F0F0"
                }

                contentItem: Text {
                    text: parent.text
                    color: "#666"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: refresh()
            }

            Button {
                text: "添加分类"
                implicitWidth: 100
                implicitHeight: 36

                background: Rectangle {
                    radius: 18
                    color: "#E3833D"
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: addCategoryPopup.open()
            }
        }

        // Categories list
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 24
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 12

                // Table header
                RowLayout {
                    Layout.fillWidth: true
                    height: 50

                    Label {
                        text: "ID"
                        font.bold: true
                        Layout.preferredWidth: 80
                    }

                    Label {
                        text: "分类名称"
                        font.bold: true
                        Layout.preferredWidth: 200
                    }

                    Label {
                        text: "排序"
                        font.bold: true
                        Layout.preferredWidth: 100
                    }

                    Label {
                        text: "状态"
                        font.bold: true
                        Layout.preferredWidth: 100
                    }

                    Item { Layout.fillWidth: true }

                    Label {
                        text: "操作"
                        font.bold: true
                        Layout.preferredWidth: 120
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#F0F0F0"
                }

                // Category list
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    model: categoryList

                    delegate: categoryRow
                }
            }
        }
    }

    // Category row
    Component {
        id: categoryRow

        Rectangle {
            width: ListView.view.width
            height: 60
            color: "transparent"

            RowLayout {
                anchors.fill: parent

                Label {
                    text: modelData.id
                    Layout.preferredWidth: 80
                    color: "#888"
                }

                Label {
                    text: modelData.name
                    font.pixelSize: 16
                    font.bold: true
                    Layout.preferredWidth: 200
                }

                Label {
                    text: modelData.sort
                    Layout.preferredWidth: 100
                    color: "#888"
                }

                Rectangle {
                    Layout.preferredWidth: 80
                    height: 28
                    radius: 14
                    color: modelData.enabled ? "#E4FFE4" : "#FFE4E4"

                    Label {
                        anchors.centerIn: parent
                        text: modelData.enabled ? "启用" : "禁用"
                        font.pixelSize: 12
                        color: modelData.enabled ? "#0A0" : "#D00"
                    }
                }

                Item { Layout.fillWidth: true }

                RowLayout {
                    Layout.preferredWidth: 120
                    spacing: 10

                    Button {
                        text: "🗑️"
                        implicitWidth: 36
                        implicitHeight: 36

                        background: Rectangle {
                            radius: 18
                            color: "#FFE4E4"
                        }

                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 16
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        onClicked: deleteCategory(modelData.id)
                    }
                }
            }
        }
    }

    // Add category popup
    AddCategoryPopup {
        id: addCategoryPopup

        onAddCategory: {
            if (apiService) {
                apiService.createCategory(category, function(success, data) {
                    if (success) {
                        refresh()
                    } else {
                        console.log("Failed to create category:", data)
                    }
                })
            }
        }
    }
}