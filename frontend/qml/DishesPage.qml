import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property var categories: []
    property var dishList: []
    property var apiService: null
    signal refresh()
    signal deleteDish(var dishId)
    signal toggleFavorite(var dishId)
    signal createDish(var dish)

    // Search/filter state
    property string searchText: ""
    property int selectedCategoryId: -1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        // Header
        RowLayout {
            Layout.fillWidth: true

            Label {
                text: "菜品管理"
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
                text: "添加菜品"
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

                onClicked: addDishPopup.open()
            }
        }

        // Search and filter
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Rectangle {
                Layout.preferredWidth: 300
                height: 44
                radius: 22
                color: "white"

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 15
                    anchors.rightMargin: 15

                    TextField {
                        id: searchField
                        placeholderText: "搜索菜品..."
                        background: null
                        Layout.fillWidth: true
                        onTextChanged: searchText = text
                    }

                    Label { text: "🔍"; font.pixelSize: 18 }
                }
            }

            // Category filter
            Rectangle {
                height: 44
                radius: 22
                color: "white"

                ComboBox {
                    anchors.fill: parent
                    anchors.margins: 4
                    model: [{ name: "全部分类", id: -1 }].concat(categories)
                    textRole: "name"
                    currentIndex: 0
                    onCurrentIndexChanged: {
                        selectedCategoryId = currentIndex === 0 ? -1 : model[currentIndex].id
                    }
                }
            }

            Item { Layout.fillWidth: true }
        }

        // Dishes grid
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            GridView {
                model: filteredDishes
                anchors.fill: parent
                cellWidth: 280
                cellHeight: 320
                clip: true

                delegate: dishCard
            }
        }
    }

    // Filtered dishes
    property var filteredDishes: {
        var result = dishList
        if (searchText) {
            var keyword = searchText.toLowerCase()
            result = result.filter(function(d) {
                return d.name.toLowerCase().indexOf(keyword) >= 0
            })
        }
        if (selectedCategoryId >= 0) {
            result = result.filter(function(d) {
                return d.category_id === selectedCategoryId
            })
        }
        return result
    }

    // Dish card component
    Component {
        id: dishCard

        Rectangle {
            width: 260
            height: 300
            radius: 20
            color: "white"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10

                // Image placeholder
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 150
                    radius: 16
                    color: "#FDE7D3"

                    Label {
                        anchors.centerIn: parent
                        text: "🍳"
                        font.pixelSize: 48
                    }
                }

                // Name
                Label {
                    text: modelData.name
                    font.pixelSize: 18
                    font.bold: true
                    elide: Text.ElideRight
                }

                // Category and difficulty
                RowLayout {
                    Label {
                        text: getCategoryName(modelData.category_id)
                        font.pixelSize: 12
                        color: "#888"
                    }

                    Item { Layout.fillWidth: true }

                    Label {
                        text: "⭐".repeat(modelData.difficulty || 1)
                        font.pixelSize: 12
                        color: "#F5A623"
                    }
                }

                // Remark
                Label {
                    text: modelData.remark || ""
                    font.pixelSize: 12
                    color: "#AAA"
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }

                Item { Layout.fillHeight: true }

                // Actions
                RowLayout {
                    Layout.fillWidth: true

                    // Favorite button
                    Button {
                        text: modelData.favorite ? "❤️" : "🤍"
                        implicitWidth: 44
                        implicitHeight: 36

                        background: Rectangle {
                            radius: 18
                            color: modelData.favorite ? "#FFE4E4" : "#F0F0F0"
                        }

                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        onClicked: toggleFavorite(modelData.id)
                    }

                    Item { Layout.fillWidth: true }

                    // Delete button
                    Button {
                        text: "🗑️"
                        implicitWidth: 44
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

                        onClicked: deleteDish(modelData.id)
                    }
                }
            }
        }
    }

    // Add dish popup
    AddDishPopup {
        id: addDishPopup
        categories: root.categories

        onAddDish: {
            if (apiService) {
                apiService.createDish(dish, function(success, data) {
                    if (success) {
                        refresh()
                    } else {
                        console.log("Failed to create dish:", data)
                    }
                })
            }
        }
    }

    function getCategoryName(categoryId) {
        for (var i = 0; i < categories.length; i++) {
            if (categories[i].id === categoryId) {
                return categories[i].name
            }
        }
        return "未分类"
    }
}