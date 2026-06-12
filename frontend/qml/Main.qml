import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1200
    height: 800
    title: "Cooks"

    // Global API Service
    ApiService {
        id: apiService
        onError: showError(message)
    }

    // Error popup
    Popup {
        id: errorPopup
        anchors.centerIn: parent
        width: 320
        height: 80
        z: 9999
        modal: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        background: Rectangle {
            radius: 16
            color: "#FFE4E4"
            border.color: "#FFCCCC"
            border.width: 2
        }

        Column {
            anchors.centerIn: parent
            spacing: 5

            Row {
                spacing: 8
                Label {
                    text: "❌"
                    font.pixelSize: 18
                }
                Label {
                    text: "错误"
                    font.pixelSize: 16
                    font.bold: true
                    color: "#D00"
                }
            }

            Label {
                id: errorMessageLabel
                font.pixelSize: 14
                color: "#800000"
                wrapMode: Text.WordWrap
                width: 280
            }
        }

        Timer {
            id: errorTimer
            interval: 3000
            onTriggered: errorPopup.close()
        }
    }

    function showError(msg) {
        errorMessageLabel.text = msg
        errorPopup.open()
        errorTimer.restart()
    }

    // Current page
    property int currentPage: 0  // 0: Home, 1: Dishes, 2: Categories, 3: History

    // Data
    property var categories: []
    property var dishes: []
    property var history: []
    property var recommendedDish: null
    property var dishStats: ({ "totalDishes": 0, "favoriteDishes": 0, "historyCount": 0 })

    // Loading state
    property bool isLoading: false

    LoginPage {
        id: loginPage
        onLoginRequested: loginHandler(user, pwd)
        onRegisterRequested: registerHandler(user, pwd, nickname)
    }

    function loginHandler(user, pwd) {
        isLoading = true
        apiService.login(user, pwd, function(success, data) {
            isLoading = false
            if (success) {
                apiService.currentUser = { username: user, nickname: user }
                showMessage("登录成功")
                loadData()
            } else {
                showMessage(data, true)
            }
        })
    }

    function registerHandler(user, pwd, nickname) {
        isLoading = true
        apiService.register(user, pwd, nickname, function(success, data) {
            isLoading = false
            if (success) {
                showMessage("注册成功，请登录")
            } else {
                showMessage(data, true)
            }
        })
    }

    // Message popup
    Popup {
        id: messagePopup
        property bool isError: false
        anchors.centerIn: parent
        width: 300
        height: 60
        z: 999
        modal: false
        closePolicy: Popup.NoAutoClose

        Rectangle {
            anchors.fill: parent
            radius: 12
            color: isError ? "#FFE4E4" : "#E4FFE4"
        }

        Label {
            id: messageLabel
            anchors.centerIn: parent
            font.pixelSize: 16
            color: isError ? "#D00" : "#0A0"
        }

        Timer {
            id: messageTimer
            interval: 2000
            onTriggered: {
                messagePopup.close()
            }
        }
    }

    function showMessage(msg, isError) {
        messageLabel.text = msg
        messagePopup.isError = isError !== undefined && isError
        messagePopup.open()
        messageTimer.restart()
        isLoading = false
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Sidebar
        Rectangle {
            Layout.preferredWidth: 220
            Layout.fillHeight: true
            color: "#FFF8F3"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 12

                Label {
                    text: "🍳 Cooks"
                    font.pixelSize: 24
                    font.bold: true
                    padding: 10
                }

                // Navigation buttons
                Repeater {
                    model: [
                        { title: "首页", icon: "🏠", page: 0 },
                        { title: "菜品", icon: "🍜", page: 1 },
                        { title: "分类", icon: "📂", page: 2 },
                        { title: "历史", icon: "📋", page: 3 }
                    ]

                    Rectangle {
                        Layout.fillWidth: true
                        height: 50
                        radius: 12
                        color: currentPage === modelData.page ? "#FDE7D3" : "transparent"

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 15

                            Label {
                                text: modelData.icon
                                font.pixelSize: 20
                            }

                            Label {
                                text: modelData.title
                                font.pixelSize: 16
                                font.bold: currentPage === modelData.page
                            }

                            Item { Layout.fillWidth: true }
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: currentPage = modelData.page
                        }
                    }
                }

                Item { Layout.fillHeight: true }

                // User info / Login button
                Rectangle {
                    Layout.fillWidth: true
                    height: 50
                    radius: 12
                    color: "#FDE7D3"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 15

                        Label {
                            text: apiService.isLoggedIn ? "👤" : "🔒"
                            font.pixelSize: 20
                        }

                        Label {
                            text: apiService.isLoggedIn ? (apiService.currentUser ? apiService.currentUser.nickname : "用户") : "未登录"
                            font.pixelSize: 14
                        }

                        Item { Layout.fillWidth: true }

                        Button {
                            text: apiService.isLoggedIn ? "退出" : "登录"
                            implicitWidth: 60
                            implicitHeight: 32
                            font.pixelSize: 12

                            background: Rectangle {
                                radius: 16
                                color: "#E3833D"
                            }

                            contentItem: Text {
                                text: parent.text
                                color: "white"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            onClicked: {
                                if (apiService.isLoggedIn) {
                                    apiService.logout()
                                    showMessage("已退出登录")
                                } else {
                                    loginPage.open()
                                }
                            }
                        }
                    }
                }

                Label {
                    text: "v1.0.0"
                    color: "#999"
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }

        // Main Content Area
        Rectangle {
            id: contentArea
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#F8F6F4"

            // Page 0: Home
            HomePage {
                visible: currentPage === 0
                anchors.fill: parent
                recommendedDish: root.recommendedDish
                stats: root.dishStats
                dishList: root.dishes
                categoryList: root.categories
                historyList: root.history
                apiService: apiService
                loginPage: loginPage

                onRefreshClicked: loadData()
                onRecommendClicked: getRandomRecommend()
            }

            // Page 1: Dishes
            DishesPage {
                visible: currentPage === 1
                anchors.fill: parent
                categories: root.categories
                dishList: root.dishes
                apiService: apiService

                onRefresh: loadDishes()
                onDeleteDish: deleteDish
                onToggleFavorite: toggleDishFavorite
            }

            // Page 2: Categories
            CategoriesPage {
                visible: currentPage === 2
                anchors.fill: parent
                categoryList: root.categories
                apiService: apiService

                onRefresh: loadCategories()
                onDeleteCategory: deleteCategory
            }

            // Page 3: History
            HistoryPage {
                visible: currentPage === 3
                anchors.fill: parent
                historyList: root.history
                dishList: root.dishes

                onRefresh: loadHistory()
                onDeleteHistory: deleteHistoryRecord
            }
        }
    }

    // Load all data
    function loadData() {
        loadCategories()
        loadDishes()
        loadHistory()
        getRandomRecommend()
    }

    function loadCategories() {
        apiService.getCategories(function(success, data) {
            if (success) {
                categories = data
            } else {
                console.log("Failed to load categories:", data)
            }
        })
    }

    function loadDishes() {
        apiService.getDishes(null, function(success, data) {
            if (success) {
                dishes = data
                // Update stats
                var favCount = 0
                for (var i = 0; i < data.length; i++) {
                    if (data[i].favorite) favCount++
                }
                dishStats = {
                    totalDishes: data.length,
                    favoriteDishes: favCount,
                    historyCount: history.length
                }
            } else {
                console.log("Failed to load dishes:", data)
            }
        })
    }

    function loadHistory() {
        apiService.getHistory(null, function(success, data) {
            if (success) {
                history = data
                dishStats.historyCount = data.length
            } else {
                console.log("Failed to load history:", data)
            }
        })
    }

    function getRandomRecommend() {
        apiService.getRandomRecommend({ exclude_days: 7 }, function(success, data) {
            if (success) {
                recommendedDish = data
            } else {
                console.log("Failed to get recommendation:", data)
            }
        })
    }

    function deleteDish(dishId) {
        apiService.deleteDish(dishId, function(success, msg) {
            showMessage(msg, !success)
            if (success) {
                loadDishes()
            }
        })
    }

    function toggleDishFavorite(dishId) {
        apiService.toggleFavorite(dishId, function(success, data) {
            if (success) {
                loadDishes()
            } else {
                showMessage(data, true)
            }
        })
    }

    function deleteCategory(categoryId) {
        apiService.deleteCategory(categoryId, function(success, msg) {
            showMessage(msg, !success)
            if (success) {
                loadCategories()
            }
        })
    }

    function deleteHistoryRecord(historyId) {
        apiService.deleteHistory(historyId, function(success, msg) {
            showMessage(msg, !success)
            if (success) {
                loadHistory()
            }
        })
    }

    // Initial load
    Component.onCompleted: {
        loadData()
    }
}