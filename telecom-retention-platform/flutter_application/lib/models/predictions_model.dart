class Recommendation {
  final String action;
  final String detail;
  final String priority;
  final String team;

  Recommendation({
    required this.action,
    required this.detail,
    required this.priority,
    required this.team,
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      action: json['action'] ?? '',
      detail: json['detail'] ?? '',
      priority: json['priority'] ?? '',
      team: json['team'] ?? '',
    );
  }
}

class PredictionResult {
  final double churnProbability;
  final String churnPrediction;
  final String confidence;
  final double revenueAtRisk;
  final List<String> riskFactors;
  final List<Recommendation> recommendations;
  final String modelUsed;
  final double modelRecall;

  PredictionResult({
    required this.churnProbability,
    required this.churnPrediction,
    required this.confidence,
    required this.revenueAtRisk,
    required this.riskFactors,
    required this.recommendations,
    required this.modelUsed,
    required this.modelRecall,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    return PredictionResult(
      churnProbability: (json['churn_probability'] ?? 0).toDouble(),
      churnPrediction: json['churn_prediction'] ?? '',
      confidence: json['confidence'] ?? '',
      revenueAtRisk:
          (json['estimated_monthly_revenue_at_risk'] ?? 0).toDouble(),
      riskFactors: List<String>.from(json['risk_factors'] ?? []),
      recommendations:
          (json['recommendations'] as List? ?? [])
              .map((r) => Recommendation.fromJson(r))
              .toList(),
      modelUsed: json['model_used'] ?? '',
      modelRecall: (json['model_recall'] ?? 0).toDouble(),
    );
  }
}

class CustomerInput {
  String gender;
  String seniorCitizen;
  String partner;
  String dependents;
  int tenure;
  String phoneService;
  String multipleLines;
  String internetService;
  String onlineSecurity;
  String onlineBackup;
  String deviceProtection;
  String techSupport;
  String streamingTV;
  String streamingMovies;
  String contract;
  String paperlessBilling;
  String paymentMethod;
  double monthlyCharges;
  double totalCharges;

  CustomerInput({
    this.gender = 'Male',
    this.seniorCitizen = 'No',
    this.partner = 'No',
    this.dependents = 'No',
    this.tenure = 1,
    this.phoneService = 'Yes',
    this.multipleLines = 'No',
    this.internetService = 'Fiber optic',
    this.onlineSecurity = 'No',
    this.onlineBackup = 'No',
    this.deviceProtection = 'No',
    this.techSupport = 'No',
    this.streamingTV = 'No',
    this.streamingMovies = 'No',
    this.contract = 'Month-to-month',
    this.paperlessBilling = 'Yes',
    this.paymentMethod = 'Electronic check',
    this.monthlyCharges = 70.0,
    this.totalCharges = 70.0,
  });

  Map<String, dynamic> toJson() => {
    'gender': gender,
    'SeniorCitizen': seniorCitizen,
    'Partner': partner,
    'Dependents': dependents,
    'tenure': tenure,
    'PhoneService': phoneService,
    'MultipleLines': multipleLines,
    'InternetService': internetService,
    'OnlineSecurity': onlineSecurity,
    'OnlineBackup': onlineBackup,
    'DeviceProtection': deviceProtection,
    'TechSupport': techSupport,
    'StreamingTV': streamingTV,
    'StreamingMovies': streamingMovies,
    'Contract': contract,
    'PaperlessBilling': paperlessBilling,
    'PaymentMethod': paymentMethod,
    'MonthlyCharges': monthlyCharges,
    'TotalCharges': totalCharges,
  };
}
