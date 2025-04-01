import 'dart:io';
import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:intl/intl.dart';
import 'package:geolocator/geolocator.dart';

class URLS {
  static const String BASE_URL = 'http://10.0.2.2:8000'; // для Android-эмулятора
}

class ApiService {
  final dio = Dio();
  final storage = FlutterSecureStorage();

  Future<Map<String, dynamic>> getMetadata() async {
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.deniedForever ||
        permission == LocationPermission.denied) {
      throw Exception("Location permission denied");
    }

    Position position = await Geolocator.getCurrentPosition();

    return {
      "timestamp": DateFormat('yyyy-MM-dd HH:mm:ss').format(DateTime.now()),
      "latitude": position.latitude,
      "longitude": position.longitude,
      "device_id": "60036017"
    };
  }

  /// Отправляет изображение и метаданные на сервер
  Future<Map<String, dynamic>> detect(File imageFile) async {
    try {
      final metadata = await getMetadata();

      FormData formData = FormData.fromMap({
        "upload_image": await MultipartFile.fromFile(imageFile.path),
        "metadata": jsonEncode(metadata)
      });

      Response response = await dio.post("${URLS.BASE_URL}/detect", data: formData);

      if (response.statusCode == 200) {
        final data = response.data;

        if (data.containsKey("message")) {
          return {
            "detections": [],
            "metadata": null
          };
        }

        List detections = data["detections"];
        return response.data;
      } else {
        return {
          "detections": [],
          "metadata": null
        };
      }
    } on DioError catch (e) {
      print("API Error: ${e.message}");
      return {
          "detections": [],
          "metadata": null
        };
    }
  }
}
