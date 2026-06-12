import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property var recommendedDish: null
    property var stats: ({ totalDishes: 0, favoriteDishes: 0, historyCount: 0 })
    property var dishList: []
    property var categoryList: []
    property var historyList: []
    property var apiService: null
    property var loginPage: null
    signal refreshClicked()
    signal recommendClicked()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        // Top right buttons
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop | Qt.AlignRight
            spacing: 10

            Button {
                text: "刷新数据"
                implicitWidth: 100
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

                onClicked: refreshClicked()
            }

            Button {
                text: apiService.isLoggedIn ? (apiService.currentUser ? apiService.currentUser.username : "已登录") : "登录"
                implicitWidth: 100
                implicitHeight: 36

                background: Rectangle {
                    radius: 18
                    color: apiService.isLoggedIn ? "#4CAF50" : "#E3833D"
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    if (apiService.isLoggedIn) {
                        // Already logged in, do nothing or show user info
                    } else {
                        loginPage.open()
                    }
                }
            }
        }

        // Main content
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 20

            // Left column
            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 20

                ColumnLayout {
                    Label {
                        text: "首页"
                        font.pixelSize: 36
                        font.bold: true
                    }

                    Label {
                        text: "发现今天的美味灵感"
                        color: "#999"
                    }
                }

                // Recommend card
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 350
                    radius: 24
                    color: "white"

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 20
                        spacing: 15

                        Label {
                            text: "今天吃什么？"
                            font.pixelSize: 28
                            font.bold: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            radius: 20
                            color: recommendedDish ? "#E3833D" : "#CCC"

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 20

                                Item { Layout.fillHeight: true }

                                Label {
                                    text: recommendedDish ? "🍳 " + recommendedDish.name : "点击下方按钮获取推荐"
                                    font.pixelSize: 36
                                    font.bold: true
                                    color: "white"
                                    Layout.alignment: Qt.AlignHCenter
                                }

                                Label {
                                    text: recommendedDish ? getCategoryName(recommendedDish.category_id) : ""
                                    color: "white"
                                    opacity: 0.9
                                    Layout.alignment: Qt.AlignHCenter
                                }

                                Item { Layout.fillHeight: true }
                            }

                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: recommendClicked()
                            }
                        }

                        Button {
                            Layout.fillWidth: true
                            implicitHeight: 50
                            text: "随机推荐一道菜"

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

                            onClicked: recommendClicked()
                        }
                    }
                }

                // Stats row
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 15

                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        radius: 16
                        color: "white"

                        Column {
                            anchors.centerIn: parent
                            Label {
                                text: root.stats.historyCount || 0
                                font.pixelSize: 28
                                font.bold: true
                                color: "#E3833D"
                            }
                            Label {
                                text: "本周已做"
                                color: "#888"
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        radius: 16
                        color: "white"

                        Column {
                            anchors.centerIn: parent
                            Label {
                                text: root.stats.favoriteDishes || 0
                                font.pixelSize: 28
                                font.bold: true
                                color: "#E3833D"
                            }
                            Label {
                                text: "收藏菜品"
                                color: "#888"
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        radius: 16
                        color: "white"

                        Column {
                            anchors.centerIn: parent
                            Label {
                                text: root.stats.totalDishes || 0
                                font.pixelSize: 28
                                font.bold: true
                                color: "#E3833D"
                            }
                            Label {
                                text: "菜品总数"
                                color: "#888"
                            }
                        }
                    }
                }
            }

            // Right column - Recent history
            Rectangle {
                Layout.preferredWidth: 320
                Layout.fillHeight: true
                radius: 24
                color: "white"

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 15

                    Label {
                        text: "最近做过"
                        font.pixelSize: 24
                        font.bold: true
                    }

                    ListView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true

                        model: historyList.slice(0, 10)

                        delegate: Rectangle {
                            width: ListView.view.width
                            height: 70
                            color: "transparent"

                            RowLayout {
                                anchors.fill: parent
                                anchors.leftMargin: 10

                                Rectangle {
                                    width: 50
                                    height: 50
                                    radius: 12
                                    color: "#FDE7D3"

                                    Label {
                                        anchors.centerIn: parent
                                        text: "🍽️"
                                        font.pixelSize: 24
                                    }
                                }

                                Column {
                                    Layout.leftMargin: 12
                                    spacing: 4

                                    Label {
                                        text: getDishName(modelData.dish_id)
                                        font.pixelSize: 16
                                        font.bold: true
                                    }

                                    Label {
                                        text: modelData.selected_method === "random" ? "🎲 随机" :
                                              modelData.selected_method === "recommend" ? "✨ 推荐" : "📝 手动"
                                        font.pixelSize: 12
                                        color: "#888"
                                    }
                                }

                                Item { Layout.fillWidth: true }

                                Label {
                                    text: formatDate(modelData.created_at)
                                    font.pixelSize: 12
                                    color: "#AAA"
                                }
                            }
                        }
                    }

                    // Tips card
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        radius: 20
                        color: "#FFF8E7"

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 15

                            Label {
                                text: "💡"
                                font.pixelSize: 32
                            }

                            Column {
                                spacing: 4

                                Label {
                                    text: "今日小贴士"
                                    font.bold: true
                                }

                                Label {
                                    text: "合理搭配荤素，营养更均衡"
                                    font.pixelSize: 12
                                    color: "#888"
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Helper functions
    function getDishName(dishId) {
        for (var i = 0; i < dishList.length; i++) {
            if (dishList[i].id === dishId) {
                return dishList[i].name
            }
        }
        return "未知菜品"
    }

    function getCategoryName(categoryId) {
        for (var i = 0; i < categoryList.length; i++) {
            if (categoryList[i].id === categoryId) {
                return categoryList[i].name
            }
        }
        return ""
    }

    function formatDate(dateStr) {
        if (!dateStr) return ""
        var date = new Date(dateStr)
        var month = date.getMonth() + 1
        var day = date.getDate()
        return month + "/" + day
    }
}