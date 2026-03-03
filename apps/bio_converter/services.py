from .models import ConversionMetrics

class ConversionEngine:
    """Service layer abstracting waste-to-energy calculations."""
    
    @staticmethod
    def get_active_metrics():
        """Retrieve the currently active standard coefficients, or defaults."""
        metrics = ConversionMetrics.objects.filter(is_active=True).first()
        if not metrics:
            return {
                'biogas_per_kg': 0.04,
                'electricity_per_m3_biogas': 2.0,
                'compost_per_kg': 0.3,
                'co2_offset_per_kg': 2.5
            }
        return {
            'biogas_per_kg': metrics.biogas_per_kg,
            'electricity_per_m3_biogas': metrics.electricity_per_m3_biogas,
            'compost_per_kg': metrics.compost_per_kg,
            'co2_offset_per_kg': metrics.co2_offset_per_kg
        }
        
    @classmethod
    def calculate(cls, weight_kg):
        """Perform calculation on given waste weight."""
        coeffs = cls.get_active_metrics()
        
        biogas_m3 = weight_kg * coeffs['biogas_per_kg']
        electricity_kwh = biogas_m3 * coeffs['electricity_per_m3_biogas']
        compost_kg = weight_kg * coeffs['compost_per_kg']
        co2_offset_kg = weight_kg * coeffs['co2_offset_per_kg']
        
        return {
            'weight_kg': float(weight_kg),
            'biogas_m3': float(round(biogas_m3, 3)),
            'electricity_kwh': float(round(electricity_kwh, 3)),
            'compost_kg': float(round(compost_kg, 3)),
            'co2_offset_kg': float(round(co2_offset_kg, 3)),
            'coefficients_used': coeffs
        }
