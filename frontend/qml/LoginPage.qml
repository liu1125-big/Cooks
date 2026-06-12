import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root
    anchors.centerIn: parent
    width: 400
    height: 520
    modal: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Rectangle {
        radius: 20
        color: "white"
    }

    signal loginRequested(string user, string pwd)
    signal registerRequested(string user, string pwd, string nickname)

    property bool isRegisterMode: false

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20

        Label {
            text: isRegisterMode ? "注册" : "登录"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: usernameField
            Layout.fillWidth: true
            placeholderText: "用户名"
            implicitHeight: 50
        }

        TextField {
            id: nicknameField
            Layout.fillWidth: true
            placeholderText: "昵称"
            implicitHeight: 50
            visible: isRegisterMode
        }

        TextField {
            id: passwordField
            Layout.fillWidth: true
            placeholderText: "密码"
            echoMode: TextInput.Password
            implicitHeight: 50
        }

        Button {
            Layout.fillWidth: true
            text: isRegisterMode ? "注册" : "登录"
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
                if (isRegisterMode) {
                    registerRequested(usernameField.text, passwordField.text, nicknameField.text)
                } else {
                    loginRequested(usernameField.text, passwordField.text)
                }
                root.close()
            }
        }

        Button {
            Layout.fillWidth: true
            text: isRegisterMode ? "返回登录" : "没有账号？立即注册"
            implicitHeight: 40

            background: Rectangle {
                radius: 20
                color: "transparent"
            }

            contentItem: Text {
                text: parent.text
                color: "#E3833D"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            onClicked: {
                isRegisterMode = !isRegisterMode
                usernameField.clear()
                nicknameField.clear()
                passwordField.clear()
            }
        }

        Button {
            Layout.fillWidth: true
            text: "取消"
            implicitHeight: 40

            background: Rectangle {
                radius: 20
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
    }
}