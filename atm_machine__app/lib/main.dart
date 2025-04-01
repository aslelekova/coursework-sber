import 'package:atm_machine__app/pages/image_picker2.dart';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
List<CameraDescription> cameras = [];
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  print(cameras);
  runApp(MaterialApp(
    theme: ThemeData(primarySwatch: Colors.lightBlue),
    initialRoute: '/image',
    routes: {
      '/image':(context) => MyHomePage(),
    },
  ));
}