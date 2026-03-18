from flask import Flask, render_template, request
from controllers.process_controller import save_file, process_file, get_last_file

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    filepath = None
    message = None

    try:
        if request.method == "POST":
            action = request.form.get("action")
            file = request.files.get("file")

            # 🔹 Upload file
            if action == "upload":
                if file and file.filename != "":
                    filepath = save_file(file)
                    message = "File berhasil diupload dan diproses"
                else:
                    message = "⚠️ Pilih file terlebih dahulu"

            # 🔹 Ambil data terakhir
            elif action == "last":
                filepath = get_last_file()
                if filepath:
                    message = "Menampilkan data terakhir"
                else:
                    message = "Belum ada file sebelumnya"

        else:
            # pertama kali buka → jangan proses apa-apa
            return render_template("upload.html", message=None)

        if filepath:
            summary = process_file(filepath)

            return render_template(
                "result.html",
                summary=summary,
                message=message
            )

    except Exception as e:
        return render_template("upload.html", message=f"Error: {str(e)}")

    return render_template("upload.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)