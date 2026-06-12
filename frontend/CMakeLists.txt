cmake_minimum_required(VERSION 3.16)

project(Cooks LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS
    Quick
    QuickControls2
)

qt_standard_project_setup()

qt_add_executable(Cooks
    main.cpp
)

qt_add_resources(Cooks resources
    PREFIX "/"

    FILES
        qml/Main.qml
        qml/LoginPage.qml
        qml/HomePage.qml
        qml/DishesPage.qml
        qml/CategoriesPage.qml
        qml/HistoryPage.qml
        qml/AddDishPopup.qml
        qml/AddCategoryPopup.qml
        qml/ApiService.qml
        qml/ModalBlur.qml
)

target_link_libraries(Cooks PRIVATE
    Qt6::Quick
    Qt6::QuickControls2
)