import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'constants/app_colors.dart';
import 'controllers/prediction_controller.dart';
import 'screens/splash_screen.dart';
import 'screens/home_screen.dart';
import 'screens/input_screen.dart';
import 'screens/results_screen.dart';
import 'screens/model_info_screen.dart';

void main() {
  runApp(const ChurnIntelligenceApp());
}

class ChurnIntelligenceApp extends StatelessWidget {
  const ChurnIntelligenceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Churn Intelligence',
      debugShowCheckedModeBanner: false,

      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.primary),
        textTheme: GoogleFonts.interTextTheme(),
        scaffoldBackgroundColor: AppColors.background,
      ),

      // Register controller globally
      initialBinding: BindingsBuilder(() {
        Get.put(PredictionController());
      }),

      // Initial route
      initialRoute: '/splash',

      // Route definitions
      getPages: [
        GetPage(name: '/splash', page: () => const SplashScreen()),
        GetPage(name: '/home', page: () => const HomeScreen()),
        GetPage(name: '/input', page: () => const InputScreen()),
        GetPage(name: '/result', page: () => const ResultScreen()),
        GetPage(name: '/model-info', page: () => const ModelInfoScreen()),
      ],
    );
  }
}
