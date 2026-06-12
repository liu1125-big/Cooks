import QtQuick

QtObject {
    function get(url, headers, callback) {
        request(url, "GET", "", headers, callback)
    }

    function post(url, body, headers, callback) {
        request(url, "POST", body, headers, callback)
    }

    function put(url, body, headers, callback) {
        request(url, "PUT", body, headers, callback)
    }

    function del(url, headers, callback) {
        request(url, "DELETE", "", headers, callback)
    }

    function request(url, method, body, headers, callback) {
        var xhr = new XMLHttpRequest()
        xhr.open(method, url)

        if (headers) {
            for (var key in headers) {
                xhr.setRequestHeader(key, headers[key])
            }
        }

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    callback(true, xhr.responseText)
                } else {
                    try {
                        var errorData = JSON.parse(xhr.responseText)
                        callback(false, errorData.detail || xhr.statusText)
                    } catch(e) {
                        callback(false, xhr.statusText || "请求失败")
                    }
                }
            }
        }

        xhr.onerror = function() {
            callback(false, "网络错误，请检查服务器是否运行")
        }

        if (body && (method === "POST" || method === "PUT")) {
            xhr.send(body)
        } else {
            xhr.send()
        }
    }
}