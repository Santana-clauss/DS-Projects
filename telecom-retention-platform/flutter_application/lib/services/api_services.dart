import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/predictions_model.dart';

class ApiService {
  // Android emulator uses 10.0.2.2 to reach host localhost
  static const String baseUrl = 'http://127.0.0.1:8000';

  // Health check
  static Future<bool> checkHealth() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(const Duration(seconds: 5));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['model_loaded'] == true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  // Single customer prediction
  static Future<PredictionResult?> predict(CustomerInput customer) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(customer.toJson()),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return PredictionResult.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  // Model info
  static Future<Map<String, dynamic>?> getModelInfo() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/model/info'))
          .timeout(const Duration(seconds: 5));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
