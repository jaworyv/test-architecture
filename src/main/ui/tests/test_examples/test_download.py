def test_download_file(page, tmp_path):

    page.goto("https://demoqa.com/upload-download")

    # Создаём временный файл для загрузки
    file_path = tmp_path / "demoqa_test_file.txt"
    file_path.write_text("Hello, this is a test file for DemoQA upload!")

    # Загружаем файл
    page.set_input_files("#uploadFile", str(file_path))

    # Проверяем, что имя файла отобразилось на странице
    uploaded_file_name = page.locator("#uploadedFilePath")
    assert file_path.name in uploaded_file_name.inner_text()