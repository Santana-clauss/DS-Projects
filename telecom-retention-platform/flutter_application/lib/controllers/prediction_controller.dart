import 'package:get/get.dart';

import '../models/predictions_model.dart';
import '../services/api_services.dart';

class PredictionController extends GetxController {
  // Observable state variables
  // Adding .obs makes GetX watch these for changes
  final isLoading = false.obs;
  final isApiHealthy = false.obs;
  final errorMessage = ''.obs;
  final Rx<PredictionResult?> predictionResult = Rx<PredictionResult?>(null);

  // Customer input object
  final customer = CustomerInput().obs;

  @override
  void onInit() {
    super.onInit();
    checkApiHealth();
  }

  // Check if API is reachable on app launch
  Future<void> checkApiHealth() async {
    isApiHealthy.value = await ApiService.checkHealth();
  }

  // Submit prediction
  Future<void> predict() async {
    if (!isApiHealthy.value) {
      errorMessage.value = 'API is not reachable. Ensure backend is running.';
      return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
      final result = await ApiService.predict(customer.value);
      if (result != null) {
        predictionResult.value = result;
        Get.toNamed('/result');
      } else {
        errorMessage.value = 'Prediction failed. Please try again.';
      }
    } catch (e) {
      errorMessage.value = 'Error: ${e.toString()}';
    } finally {
      isLoading.value = false;
    }
  }

  // Update customer field
  void updateCustomer(CustomerInput updated) {
    customer.value = updated;
  }

  // Reset for new prediction
  void reset() {
    predictionResult.value = null;
    errorMessage.value = '';
    customer.value = CustomerInput();
  }

  // Risk color helper
  String getRiskColor(String prediction) {
    switch (prediction) {
      case 'High Risk':
        return 'high';
      case 'Medium Risk':
        return 'medium';
      default:
        return 'low';
    }
  }
}
