import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import '../constants/app_colors.dart';
import '../controllers/prediction_controller.dart';
import '../models/predictions_model.dart';


class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final controller = Get.find<PredictionController>();
  final _formKey = GlobalKey<FormState>();
  late CustomerInput _input;

  // Dropdown options
  final _yesNo = ['Yes', 'No'];
  final _genders = ['Male', 'Female'];
  final _multiLines = ['Yes', 'No', 'No phone service'];
  final _internet = ['DSL', 'Fiber optic', 'No'];
  final _addOn = ['Yes', 'No', 'No internet service'];
  final _contracts = ['Month-to-month', 'One year', 'Two year'];
  final _payments = [
    'Electronic check',
    'Mailed check',
    'Bank transfer (automatic)',
    'Credit card (automatic)',
  ];

  @override
  void initState() {
    super.initState();
    _input = controller.customer.value;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.primary,
        elevation: 0,
        title: Text(
          'Customer Details',
          style: GoogleFonts.inter(
            fontSize: 17,
            fontWeight: FontWeight.w600,
            color: Colors.white,
          ),
        ),
        leading: IconButton(
          icon: const Icon(
            Icons.arrow_back_ios_rounded,
            color: Colors.white,
            size: 18,
          ),
          onPressed: () => Get.back(),
        ),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _sectionTitle('Demographics'),
              _dropdown(
                'Gender',
                _genders,
                _input.gender,
                (v) => setState(() => _input.gender = v!),
              ),
              _dropdown(
                'Senior Citizen',
                _yesNo,
                _input.seniorCitizen,
                (v) => setState(() => _input.seniorCitizen = v!),
              ),
              _dropdown(
                'Partner',
                _yesNo,
                _input.partner,
                (v) => setState(() => _input.partner = v!),
              ),
              _dropdown(
                'Dependents',
                _yesNo,
                _input.dependents,
                (v) => setState(() => _input.dependents = v!),
              ),

              const SizedBox(height: 8),
              _sectionTitle('Account Information'),
              _numberField(
                'Tenure (months)',
                _input.tenure.toString(),
                (v) => setState(() => _input.tenure = int.tryParse(v) ?? 1),
              ),
              _numberField(
                'Monthly Charges (\$)',
                _input.monthlyCharges.toString(),
                (v) => setState(
                  () => _input.monthlyCharges = double.tryParse(v) ?? 0,
                ),
              ),
              _numberField(
                'Total Charges (\$)',
                _input.totalCharges.toString(),
                (v) => setState(
                  () => _input.totalCharges = double.tryParse(v) ?? 0,
                ),
              ),

              const SizedBox(height: 8),
              _sectionTitle('Contract & Billing'),
              _dropdown(
                'Contract',
                _contracts,
                _input.contract,
                (v) => setState(() => _input.contract = v!),
              ),
              _dropdown(
                'Payment Method',
                _payments,
                _input.paymentMethod,
                (v) => setState(() => _input.paymentMethod = v!),
              ),
              _dropdown(
                'Paperless Billing',
                _yesNo,
                _input.paperlessBilling,
                (v) => setState(() => _input.paperlessBilling = v!),
              ),

              const SizedBox(height: 8),
              _sectionTitle('Services'),
              _dropdown(
                'Phone Service',
                _yesNo,
                _input.phoneService,
                (v) => setState(() => _input.phoneService = v!),
              ),
              _dropdown(
                'Multiple Lines',
                _multiLines,
                _input.multipleLines,
                (v) => setState(() => _input.multipleLines = v!),
              ),
              _dropdown(
                'Internet Service',
                _internet,
                _input.internetService,
                (v) => setState(() => _input.internetService = v!),
              ),
              _dropdown(
                'Online Security',
                _addOn,
                _input.onlineSecurity,
                (v) => setState(() => _input.onlineSecurity = v!),
              ),
              _dropdown(
                'Online Backup',
                _addOn,
                _input.onlineBackup,
                (v) => setState(() => _input.onlineBackup = v!),
              ),
              _dropdown(
                'Tech Support',
                _addOn,
                _input.techSupport,
                (v) => setState(() => _input.techSupport = v!),
              ),
              _dropdown(
                'Streaming TV',
                _addOn,
                _input.streamingTV,
                (v) => setState(() => _input.streamingTV = v!),
              ),
              _dropdown(
                'Streaming Movies',
                _addOn,
                _input.streamingMovies,
                (v) => setState(() => _input.streamingMovies = v!),
              ),

              const SizedBox(height: 24),

              // Error message
              Obx(
                () =>
                    controller.errorMessage.value.isNotEmpty
                        ? Container(
                          padding: const EdgeInsets.all(12),
                          margin: const EdgeInsets.only(bottom: 12),
                          decoration: BoxDecoration(
                            color: AppColors.highRisk.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(
                              color: AppColors.highRisk.withOpacity(0.3),
                            ),
                          ),
                          child: Text(
                            controller.errorMessage.value,
                            style: GoogleFonts.inter(
                              fontSize: 13,
                              color: AppColors.highRisk,
                            ),
                          ),
                        )
                        : const SizedBox.shrink(),
              ),

              // Predict button
              Obx(
                () => SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: ElevatedButton(
                    onPressed:
                        controller.isLoading.value
                            ? null
                            : () {
                              controller.updateCustomer(_input);
                              controller.predict();
                            },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      disabledBackgroundColor: AppColors.primary.withOpacity(
                        0.5,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14),
                      ),
                      elevation: 0,
                    ),
                    child:
                        controller.isLoading.value
                            ? const SizedBox(
                              width: 22,
                              height: 22,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  Colors.white,
                                ),
                              ),
                            )
                            : Text(
                              'Predict Churn Risk',
                              style: GoogleFonts.inter(
                                fontSize: 15,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                  ),
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  // ── Helper Widgets ─────────────────────────────────────────

  Widget _sectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10, top: 4),
      child: Text(
        title,
        style: GoogleFonts.inter(
          fontSize: 13,
          fontWeight: FontWeight.w600,
          color: AppColors.textSecondary,
          letterSpacing: 0.5,
        ),
      ),
    );
  }

  Widget _dropdown(
    String label,
    List<String> options,
    String value,
    void Function(String?) onChanged,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: DropdownButtonFormField<String>(
        value: options.contains(value) ? value : options.first,
        decoration: InputDecoration(
          labelText: label,
          labelStyle: GoogleFonts.inter(
            fontSize: 12,
            color: AppColors.textSecondary,
          ),
          border: InputBorder.none,
        ),
        items:
            options
                .map(
                  (o) => DropdownMenuItem(
                    value: o,
                    child: Text(o, style: GoogleFonts.inter(fontSize: 13)),
                  ),
                )
                .toList(),
        onChanged: onChanged,
        style: GoogleFonts.inter(fontSize: 13, color: AppColors.textPrimary),
        dropdownColor: AppColors.surface,
        icon: const Icon(Icons.keyboard_arrow_down_rounded, size: 20),
      ),
    );
  }

  Widget _numberField(
    String label,
    String initial,
    void Function(String) onChanged,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: TextFormField(
        initialValue: initial,
        keyboardType: TextInputType.number,
        onChanged: onChanged,
        style: GoogleFonts.inter(fontSize: 13, color: AppColors.textPrimary),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: GoogleFonts.inter(
            fontSize: 12,
            color: AppColors.textSecondary,
          ),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 14,
            vertical: 14,
          ),
          border: InputBorder.none,
        ),
      ),
    );
  }
}
