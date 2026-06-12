import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property var historyList: []
    property var dishList: []
    signal refresh()
    signal deleteHistory(var historyId)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        // Header
        RowLayout {
            Layout.fillWidth: true

            Label {
                text: "历史记录"
                font.pixelSize: 36
                font.bold: true
            }

            Label {
                text: "(" + historyList.length + "条记录)"
                font.pixelSize: 18
                color: "#888"
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
        }

        // History list
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
                        Layout.preferredWidth: 60
                    }

                    Label {
                        text: "菜品"
                        font.bold: true
                        Layout.preferredWidth: 150
                    }

                    Label {
                        text: "选择方式"
                        font.bold: true
                        Layout.preferredWidth: 120
                    }

                    Label {
                        text: "备注"
                        font.bold: true
                        Layout.preferredWidth: 200
                    }

                    Label {
                        text: "时间"
                        font.bold: true
                        Layout.preferredWidth: 150
                    }

                    Item { Layout.fillWidth: true }

                    Label {
                        text: "操作"
                        font.bold: true
                        Layout.preferredWidth: 80
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#F0F0F0"
                }

                // History list
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    model: historyList

                    delegate: historyRow
                }
            }
        }
    }

    // History row
    Component {
        id: historyRow

        Rectangle {
            width: ListView.view.width
            height: 70
            color: "transparent"

            RowLayout {
                anchors.fill: parent

                Label {
                    text: modelData.id
                    Layout.preferredWidth: 60
                    color: "#888"
                }

                Label {
                    text: getDishName(modelData.dish_id)
                    font.pixelSize: 16
                    font.bold: true
                    Layout.preferredWidth: 150
                }

                Rectangle {
                    Layout.preferredWidth: 100
                    height: 28
                    radius: 14
                    color: getMethodColor(modelData.selected_method)

                    Label {
                        anchors.centerIn: parent
                        text: getMethodText(modelData.selected_method)
                        font.pixelSize: 12
                    }
                }

                Label {
                    text: modelData.comment || "-"
                    font.pixelSize: 14
                    color: "#666"
                    Layout.preferredWidth: 200
                    elide: Text.ElideRight
                }

                Label {
                    text: formatDate(modelData.created_at)
                    font.pixelSize: 14
                    color: "#888"
                    Layout.preferredWidth: 150
                }

                Item { Layout.fillWidth: true }

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

                    onClicked: deleteHistory(modelData.id)
                }
            }
        }
    }

    function getDishName(dishId) {
        for (var i = 0; i < dishList.length; i++) {
            if (dishList[i].id === dishId) {
                return dishList[i].name
            }
        }
        return "未知菜品"
    }

    function getMethodText(method) {
        switch(method) {
            case "random": return "🎲 随机"
            case "recommend": return "✨ 推荐"
            case "manual": return "📝 手动"
            default: return method
        }
    }

    function getMethodColor(method) {
        switch(method) {
            case "random": return "#E4F0FF"
            case "recommend": return "#FFF4E4"
            case "manual": return "#F0FFE4"
            default: return "#F0F0F0"
        }
    }

    function formatDate(dateStr) {
        if (!dateStr) return ""
        var date = new Date(dateStr)
        var year = date.getFullYear()
        var month = date.getMonth() + 1
        var day = date.getDate()
        var hour = date.getHours()
        var minute = date.getMinutes()
        return year + "-" + (month < 10 ? "0" : "") + month + "-" + (day < 10 ? "0" : "") + day + " " + (hour < 10 ? "0" : "") + hour + ":" + (minute < 10 ? "0" : "") + minute
    }
}