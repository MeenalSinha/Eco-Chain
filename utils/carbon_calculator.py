"""
Carbon Calculator Module
Calculates CO2 emissions based on energy consumption and business type
"""

class CarbonCalculator:
    """
    Calculates carbon emissions from energy consumption
    Uses emission factors from IEA and EPA standards
    """
    
    # CO2 emission factors (kg CO2 per kWh)
    # Based on average grid emission factors by region/industry
    EMISSION_FACTORS = {
        'grid_electricity': 0.92,  # kg CO2 per kWh (India average)
        'natural_gas': 0.185,      # kg CO2 per kWh
        'diesel': 0.267,           # kg CO2 per kWh
        'solar': 0.05,             # kg CO2 per kWh (lifecycle)
        'wind': 0.02,              # kg CO2 per kWh (lifecycle)
    }
    
    # Industry-specific baseline emissions (kg CO2 per kWh)
    # Represents typical industry performance
    INDUSTRY_BASELINES = {
        'Manufacturing': 1.05,
        'Textile': 1.15,
        'Food Processing': 0.95,
        'Retail': 0.85,
        'Technology': 0.90,
        'default': 1.0
    }
    
    # Efficiency multipliers
    EFFICIENCY_FACTORS = {
        'low': 1.2,      # Old equipment, poor maintenance
        'medium': 1.0,   # Standard equipment
        'high': 0.85,    # Modern, well-maintained equipment
    }
    
    def __init__(self):
        pass
    
    def calculate_emissions(self, energy_kwh, business_type='default', 
                          renewable_pct=0, efficiency=80):
        """
        Calculate CO2 emissions from energy consumption
        
        Args:
            energy_kwh: Energy consumption in kilowatt-hours
            business_type: Type of business (affects emission factors)
            renewable_pct: Percentage of renewable energy (0-100)
            efficiency: Equipment efficiency percentage (0-100)
        
        Returns:
            float: CO2 emissions in kilograms
        """
        # Validate inputs
        if energy_kwh < 0:
            raise ValueError("Energy consumption cannot be negative")
        if not 0 <= renewable_pct <= 100:
            raise ValueError("Renewable percentage must be between 0 and 100")
        if not 0 <= efficiency <= 100:
            raise ValueError("Efficiency must be between 0 and 100")
        
        # Calculate base emissions from grid electricity
        renewable_fraction = renewable_pct / 100
        grid_fraction = 1 - renewable_fraction
        
        # Grid electricity emissions
        grid_emissions = energy_kwh * grid_fraction * self.EMISSION_FACTORS['grid_electricity']
        
        # Renewable energy emissions (minimal lifecycle emissions)
        renewable_emissions = energy_kwh * renewable_fraction * self.EMISSION_FACTORS['solar']
        
        # Total base emissions
        base_emissions = grid_emissions + renewable_emissions
        
        # Apply efficiency factor
        efficiency_multiplier = self._get_efficiency_multiplier(efficiency)
        adjusted_emissions = base_emissions * efficiency_multiplier
        
        # Apply industry-specific adjustments
        industry_factor = self._get_industry_factor(business_type)
        final_emissions = adjusted_emissions * industry_factor
        
        return round(final_emissions, 2)
    
    def get_baseline_emissions(self, energy_kwh, business_type='default'):
        """
        Get baseline emissions for comparison (industry average)
        
        Args:
            energy_kwh: Energy consumption in kilowatt-hours
            business_type: Type of business
        
        Returns:
            float: Baseline CO2 emissions in kilograms
        """
        baseline_factor = self.INDUSTRY_BASELINES.get(
            business_type, 
            self.INDUSTRY_BASELINES['default']
        )
        
        return round(energy_kwh * baseline_factor, 2)
    
    def calculate_reduction_percentage(self, actual_emissions, baseline_emissions):
        """
        Calculate the percentage reduction vs baseline
        
        Args:
            actual_emissions: Actual CO2 emissions
            baseline_emissions: Baseline CO2 emissions
        
        Returns:
            float: Reduction percentage
        """
        if baseline_emissions == 0:
            return 0
        
        reduction = baseline_emissions - actual_emissions
        reduction_pct = (reduction / baseline_emissions) * 100
        
        return round(reduction_pct, 2)
    
    def _get_efficiency_multiplier(self, efficiency_pct):
        """
        Convert efficiency percentage to emissions multiplier
        
        Args:
            efficiency_pct: Equipment efficiency (0-100)
        
        Returns:
            float: Emissions multiplier
        """
        if efficiency_pct >= 85:
            return self.EFFICIENCY_FACTORS['high']
        elif efficiency_pct >= 70:
            return self.EFFICIENCY_FACTORS['medium']
        else:
            return self.EFFICIENCY_FACTORS['low']
    
    def _get_industry_factor(self, business_type):
        """
        Get industry-specific emissions factor
        
        Args:
            business_type: Type of business
        
        Returns:
            float: Industry factor
        """
        # Normalize for consistent calculation
        # Most industries are already accounted for in baseline
        # This is for additional fine-tuning
        return 1.0
    
    def get_emission_breakdown(self, energy_kwh, renewable_pct=0):
        """
        Get detailed breakdown of emissions sources
        
        Args:
            energy_kwh: Total energy consumption
            renewable_pct: Percentage of renewable energy
        
        Returns:
            dict: Breakdown of emissions by source
        """
        renewable_fraction = renewable_pct / 100
        grid_fraction = 1 - renewable_fraction
        
        breakdown = {
            'grid_electricity': {
                'kwh': energy_kwh * grid_fraction,
                'emissions': energy_kwh * grid_fraction * self.EMISSION_FACTORS['grid_electricity']
            },
            'renewable': {
                'kwh': energy_kwh * renewable_fraction,
                'emissions': energy_kwh * renewable_fraction * self.EMISSION_FACTORS['solar']
            },
            'total': energy_kwh
        }
        
        return breakdown
    
    def estimate_cost_savings(self, emissions_reduced, carbon_price=25):
        """
        Estimate financial value of emissions reduction
        
        Args:
            emissions_reduced: CO2 reduced in kg
            carbon_price: Price per ton of CO2 (USD)
        
        Returns:
            float: Estimated cost savings in USD
        """
        # Convert kg to tons
        emissions_tons = emissions_reduced / 1000
        
        # Calculate savings
        savings = emissions_tons * carbon_price
        
        return round(savings, 2)
    
    def calculate_tree_equivalent(self, co2_kg):
        """
        Convert CO2 emissions to tree equivalents
        (Average tree absorbs ~21 kg CO2 per year)
        
        Args:
            co2_kg: CO2 in kilograms
        
        Returns:
            float: Number of trees needed to offset
        """
        CO2_PER_TREE_YEAR = 21  # kg
        trees = co2_kg / CO2_PER_TREE_YEAR
        
        return round(trees, 2)
