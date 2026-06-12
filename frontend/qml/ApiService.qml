import QtQuick

QtObject {
    // API Base URL
    readonly property string baseUrl: "http://127.0.0.1:8001"

    // Token storage
    property string accessToken: ""

    // Check if user is logged in
    property bool isLoggedIn: accessToken !== ""

    // Current user info
    property var currentUser: null

    // Error signal for global error handling
    signal error(string message)

    // Get headers for authenticated requests
    function authHeaders() {
        var headers = { "Content-Type": "application/json" }
        if (accessToken) {
            headers["Authorization"] = "Bearer " + accessToken
        }
        return headers
    }

    // ==================== Auth APIs ====================

    function login(username, password, callback) {
        var body = JSON.stringify({ username: username, password: password })
        post(baseUrl + "/api/users/login", body, { "Content-Type": "application/json" }, function(success, data) {
            if (success && data.access_token) {
                accessToken = data.access_token
            }
            callback(success, data)
        })
    }

    function register(username, password, nickname, callback) {
        var body = JSON.stringify({
            username: username,
            password: password,
            nickname: nickname || username,
            role: "user"
        })
        post(baseUrl + "/api/users/register", body, { "Content-Type": "application/json" }, callback, true)
    }

    function logout() {
        accessToken = ""
        currentUser = null
    }

    // ==================== Dish APIs ====================

    function getDishes(params, callback) {
        var query = ""
        if (params) {
            var parts = []
            if (params.keyword) parts.push("keyword=" + encodeURIComponent(params.keyword))
            if (params.category_id !== undefined) parts.push("category_id=" + params.category_id)
            if (params.favorite !== undefined) parts.push("favorite=" + params.favorite)
            if (params.difficulty !== undefined) parts.push("difficulty=" + params.difficulty)
            if (params.enabled !== undefined) parts.push("enabled=" + params.enabled)
            if (parts.length > 0) query = "?" + parts.join("&")
        }
        get(baseUrl + "/api/dishes" + query, authHeaders(), callback)
    }

    function getDish(dishId, callback) {
        get(baseUrl + "/api/dishes/" + dishId, authHeaders(), callback)
    }

    function createDish(dish, callback) {
        var body = JSON.stringify(dish)
        post(baseUrl + "/api/dishes", body, authHeaders(), callback)
    }

    function updateDish(dishId, dish, callback) {
        var body = JSON.stringify(dish)
        put(baseUrl + "/api/dishes/" + dishId, body, authHeaders(), callback)
    }

    function deleteDish(dishId, callback) {
        del(baseUrl + "/api/dishes/" + dishId, authHeaders(), callback)
    }

    function toggleFavorite(dishId, callback) {
        post(baseUrl + "/api/dishes/" + dishId + "/favorite", "", authHeaders(), callback)
    }

    // ==================== Category APIs ====================

    function getCategories(callback) {
        get(baseUrl + "/api/categories", { "Content-Type": "application/json" }, callback)
    }

    function createCategory(category, callback) {
        var body = JSON.stringify(category)
        post(baseUrl + "/api/categories", body, authHeaders(), callback)
    }

    function updateCategory(categoryId, category, callback) {
        var body = JSON.stringify(category)
        put(baseUrl + "/api/categories/" + categoryId, body, authHeaders(), callback)
    }

    function deleteCategory(categoryId, callback) {
        del(baseUrl + "/api/categories/" + categoryId, authHeaders(), callback)
    }

    // ==================== History APIs ====================

    function getHistory(params, callback) {
        var query = ""
        if (params) {
            var parts = []
            if (params.start_date) parts.push("start_date=" + encodeURIComponent(params.start_date))
            if (params.end_date) parts.push("end_date=" + encodeURIComponent(params.end_date))
            if (params.dish_id !== undefined) parts.push("dish_id=" + params.dish_id)
            if (parts.length > 0) query = "?" + parts.join("&")
        }
        get(baseUrl + "/api/history" + query, authHeaders(), callback)
    }

    function createHistory(history, callback) {
        var body = JSON.stringify(history)
        post(baseUrl + "/api/history", body, authHeaders(), callback)
    }

    function deleteHistory(historyId, callback) {
        del(baseUrl + "/api/history/" + historyId, authHeaders(), callback)
    }

    // ==================== Recommend APIs ====================

    function getRandomRecommend(params, callback) {
        var query = ""
        if (params) {
            var parts = []
            if (params.category_id !== undefined) parts.push("category_id=" + params.category_id)
            if (params.exclude_days !== undefined) parts.push("exclude_days=" + params.exclude_days)
            if (parts.length > 0) query = "?" + parts.join("&")
        }
        get(baseUrl + "/recommend/random" + query, { "Content-Type": "application/json" }, callback)
    }

    // ==================== User APIs ====================

    function getUsers(callback) {
        get(baseUrl + "/api/users", authHeaders(), callback)
    }

    function getUser(userId, callback) {
        get(baseUrl + "/api/users/" + userId, authHeaders(), callback)
    }

    // ==================== HTTP Methods ====================

    function get(url, headers, callback) {
        request(url, "GET", "", headers, callback)
    }

    function post(url, body, headers, callback, parseResponse) {
        request(url, "POST", body, headers, callback, parseResponse)
    }

    function put(url, body, headers, callback) {
        request(url, "PUT", body, headers, callback)
    }

    function del(url, headers, callback) {
        request(url, "DELETE", "", headers, callback)
    }

    function request(url, method, body, headers, callback, parseResponse) {
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
                    if (parseResponse === false) {
                        callback(true, xhr.responseText)
                    } else {
                        try {
                            callback(true, JSON.parse(xhr.responseText))
                        } catch(e) {
                            callback(false, "解析响应失败")
                            error("解析响应失败")
                        }
                    }
                } else {
                    var errorMsg = ""
                    try {
                        var errorData = JSON.parse(xhr.responseText)
                        errorMsg = errorData.detail || xhr.statusText
                    } catch(e) {
                        errorMsg = xhr.statusText || "请求失败"
                    }
                    callback(false, errorMsg)
                    error(errorMsg)
                }
            }
        }

        xhr.onerror = function() {
            var errorMsg = "网络错误，请检查服务器是否运行"
            callback(false, errorMsg)
            error(errorMsg)
        }

        if (body && (method === "POST" || method === "PUT")) {
            xhr.send(body)
        } else {
            xhr.send()
        }
    }
}