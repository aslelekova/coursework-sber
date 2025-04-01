import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../moduls/api.dart';

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late File? _image;
  final api = ApiService();

  @override
  void initState() {
    super.initState();
    _image = null;
  }

  Future<void> _getImageFromCamera() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.camera);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
      } else {
        print('No image selected.');
      }
    });

    if (pickedFile != null) {
      Map<String, dynamic> res = await api.detect(_image!);
      _showResults(res);
    }
  }

  Future<void> _getImageFromGallery() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
      } else {
        print('No image selected.');
      }
    });

    if (pickedFile != null) {
      final res = await api.detect(_image!);
      _showResults(res);
    }
  }

  void _showResults(Map<String, dynamic> res) {
    final metadata = res['metadata'];
    final detections = List<Map<String, dynamic>>.from(res['detections']);

    if (detections.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Банкоматы не найдены")),
      );
      return;
    }

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text("Результаты классификации"),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ...detections.map((item) {
                final label = item['classification'];
                final confidence = (item['confidence'] * 100).toStringAsFixed(1);
                final box = item['box'];

                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ListTile(
                      leading: Icon(
                        label == 'clean' ? Icons.check_circle : Icons.warning,
                        color: label == 'clean' ? Colors.green : Colors.red,
                      ),
                      title: Text("Координаты: {x1: ${box['x1']}, y1: ${box['y1']}, x2: ${box['x2']}, y2: ${box['y2']}}"),
                      subtitle: Text("$label (уверенность: $confidence%)"),
                    ),
                    Divider(),
                  ],
                );
              }),
              if (metadata != null) ...[
                SizedBox(height: 10),
                Text("Дата и время: ${metadata['datetime']}", style: TextStyle(fontWeight: FontWeight.bold))
              ]
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text("ОК"),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Center(
            child: _image == null
              ? ClipOval(
                  child: Image.asset(
                    "assets/logo.png",
                    width: 150,
                    height: 150,
                    fit: BoxFit.cover,
                  ),
                )
              : Image.file(_image!)
          ),
          _image != null
              ? Positioned(
                  top: 0,
                  left: 0,
                  right: 0,
                  child: AppBar(
                    backgroundColor: Color.fromARGB(255, 0, 150, 70),
                    toolbarHeight: MediaQuery.of(context).size.width * 0.25,
                    title: Center(
                      child: Text(
                        'ATM Classification',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 24,
                        ),
                      ),
                    ),
                  ),
                )
              : Container(),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(0, 20, 0, 20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: 145.0,
                    height: 80.0,
                    child: RawMaterialButton(
                      onPressed: _getImageFromCamera,
                      elevation: 2.0,
                      fillColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      child: Icon(
                        Icons.camera,
                        size: 32.0,
                        color: Color.fromARGB(255, 0, 150, 70),
                      ),
                    ),
                  ),
                  SizedBox(width: 28),
                  SizedBox(
                    width: 145.0,
                    height: 80.0,
                    child: RawMaterialButton(
                      onPressed: _getImageFromGallery,
                      elevation: 2.0,
                      fillColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      child: Icon(
                        Icons.image,
                        size: 32.0,
                        color: Color.fromARGB(255, 0, 150, 70),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
