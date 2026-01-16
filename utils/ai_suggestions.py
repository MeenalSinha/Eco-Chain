"""
AI Sustainability Suggester Module
Provides rule-based sustainability improvement suggestions
"""

class SustainabilitySuggester:
    """
    Generates personalized sustainability suggestions based on business type and performance
    Uses rule-based logic to provide actionable recommendations
    """
    
    def __init__(self):
        # Industry-specific suggestions database
        self.suggestions_db = {
            'Manufacturing': {
                'energy_efficiency': {
                    'title': 'Upgrade to Energy-Efficient Machinery',
                    'description': 'Replace old motors and equipment with modern, energy-efficient alternatives that meet or exceed BEE 5-star ratings.',
                    'steps': [
                        'Conduct energy audit of all machinery',
                        'Identify equipment older than 10 years',
                        'Compare energy consumption with modern alternatives',
                        'Calculate ROI for replacement',
                        'Apply for government subsidies (SIDBI, MSME schemes)'
                    ],
                    'impact': 'High (15-25% reduction)',
                    'co2_reduction': '150-300 kg/month',
                    'cost': '₹2-5 lakhs',
                    'payback': '2-3 years',
                    'priority': 'High'
                },
                'solar_power': {
                    'title': 'Install Rooftop Solar Panels',
                    'description': 'Generate clean energy on-site to reduce grid dependency and lower emissions significantly.',
                    'steps': [
                        'Assess rooftop space and orientation',
                        'Get solar potential assessment',
                        'Choose between on-grid or hybrid system',
                        'Apply for PM-KUSUM or state solar subsidies',
                        'Install 10-50 kW system based on consumption'
                    ],
                    'impact': 'Very High (30-50% reduction)',
                    'co2_reduction': '400-800 kg/month',
                    'cost': '₹50,000-3 lakhs',
                    'payback': '4-6 years',
                    'priority': 'Very High'
                },
                'lighting': {
                    'title': 'Switch to LED Lighting',
                    'description': 'Replace all fluorescent and incandescent bulbs with LED alternatives.',
                    'steps': [
                        'Count all lighting fixtures',
                        'Calculate current wattage',
                        'Purchase BEE-certified LED bulbs',
                        'Replace all lights in factory floor first',
                        'Add motion sensors in storage areas'
                    ],
                    'impact': 'Medium (8-12% reduction)',
                    'co2_reduction': '80-120 kg/month',
                    'cost': '₹20,000-50,000',
                    'payback': '6-12 months',
                    'priority': 'High'
                },
                'load_shifting': {
                    'title': 'Implement Load Shifting Strategy',
                    'description': 'Schedule energy-intensive operations during off-peak hours to leverage lower grid emissions.',
                    'steps': [
                        'Identify peak vs off-peak tariff hours',
                        'List energy-intensive processes',
                        'Reschedule batch operations to night shift',
                        'Install time-based automation',
                        'Monitor and optimize scheduling monthly'
                    ],
                    'impact': 'Medium (10-15% reduction)',
                    'co2_reduction': '100-150 kg/month',
                    'cost': '₹10,000-30,000',
                    'payback': '3-6 months',
                    'priority': 'Medium'
                }
            },
            'Textile': {
                'water_heating': {
                    'title': 'Optimize Water Heating Systems',
                    'description': 'Use solar water heaters and insulate pipes to reduce energy waste in dyeing and washing processes.',
                    'steps': [
                        'Install solar water heating system',
                        'Insulate all hot water pipes',
                        'Use heat recovery from wastewater',
                        'Optimize temperature settings',
                        'Regular maintenance of boilers'
                    ],
                    'impact': 'High (20-30% reduction)',
                    'co2_reduction': '200-350 kg/month',
                    'cost': '₹1-3 lakhs',
                    'payback': '2-3 years',
                    'priority': 'High'
                },
                'dryer_efficiency': {
                    'title': 'Improve Dryer Efficiency',
                    'description': 'Upgrade to heat-pump dryers or use waste heat recovery systems.',
                    'steps': [
                        'Audit current drying energy consumption',
                        'Consider heat pump dryers',
                        'Install heat recovery ventilators',
                        'Optimize drying cycles',
                        'Regular filter cleaning schedule'
                    ],
                    'impact': 'Medium (15-20% reduction)',
                    'co2_reduction': '150-200 kg/month',
                    'cost': '₹1.5-4 lakhs',
                    'payback': '2-4 years',
                    'priority': 'Medium'
                }
            },
            'Food Processing': {
                'refrigeration': {
                    'title': 'Upgrade Refrigeration Systems',
                    'description': 'Replace old refrigeration units with modern, inverter-based systems.',
                    'steps': [
                        'Audit all cooling equipment',
                        'Check refrigerant types (avoid HFCs)',
                        'Install inverter-based compressors',
                        'Improve insulation of cold rooms',
                        'Regular maintenance schedule'
                    ],
                    'impact': 'Very High (25-35% reduction)',
                    'co2_reduction': '300-400 kg/month',
                    'cost': '₹2-5 lakhs',
                    'payback': '2-3 years',
                    'priority': 'Very High'
                },
                'waste_heat': {
                    'title': 'Capture and Reuse Waste Heat',
                    'description': 'Install heat exchangers to capture waste heat from ovens and boilers.',
                    'steps': [
                        'Identify waste heat sources',
                        'Calculate available heat energy',
                        'Install heat recovery units',
                        'Use for water preheating',
                        'Monitor energy savings'
                    ],
                    'impact': 'High (15-25% reduction)',
                    'co2_reduction': '150-250 kg/month',
                    'cost': '₹1-2 lakhs',
                    'payback': '1-2 years',
                    'priority': 'High'
                }
            },
            'Retail': {
                'hvac': {
                    'title': 'Optimize HVAC Systems',
                    'description': 'Use smart thermostats and zoned cooling to reduce air conditioning energy.',
                    'steps': [
                        'Install programmable thermostats',
                        'Create cooling zones',
                        'Regular AC maintenance',
                        'Seal air leaks in building',
                        'Consider thermal curtains'
                    ],
                    'impact': 'High (20-30% reduction)',
                    'co2_reduction': '180-280 kg/month',
                    'cost': '₹50,000-1.5 lakhs',
                    'payback': '1-2 years',
                    'priority': 'High'
                },
                'daylight': {
                    'title': 'Maximize Natural Lighting',
                    'description': 'Use skylights and reflective surfaces to reduce artificial lighting needs.',
                    'steps': [
                        'Install skylights where possible',
                        'Use light tubes for interior spaces',
                        'Paint walls with light colors',
                        'Install light sensors',
                        'Clean windows regularly'
                    ],
                    'impact': 'Medium (10-15% reduction)',
                    'co2_reduction': '90-140 kg/month',
                    'cost': '₹30,000-80,000',
                    'payback': '1-2 years',
                    'priority': 'Medium'
                }
            },
            'Technology': {
                'server_efficiency': {
                    'title': 'Optimize Server and Data Center Cooling',
                    'description': 'Implement hot aisle/cold aisle containment and use fresh air cooling.',
                    'steps': [
                        'Reorganize server racks',
                        'Implement containment strategy',
                        'Increase cooling temperature setpoint',
                        'Use economizer mode when possible',
                        'Virtualize underutilized servers'
                    ],
                    'impact': 'High (20-30% reduction)',
                    'co2_reduction': '200-320 kg/month',
                    'cost': '₹50,000-2 lakhs',
                    'payback': '1-2 years',
                    'priority': 'High'
                },
                'power_management': {
                    'title': 'Implement Power Management Policies',
                    'description': 'Enable sleep modes and power-down schedules for all equipment.',
                    'steps': [
                        'Enable power management on all PCs',
                        'Set monitors to sleep after 5 minutes',
                        'Schedule automatic shutdown at night',
                        'Use smart power strips',
                        'Educate staff on power saving'
                    ],
                    'impact': 'Medium (10-15% reduction)',
                    'co2_reduction': '100-150 kg/month',
                    'cost': '₹5,000-15,000',
                    'payback': '2-4 months',
                    'priority': 'High'
                }
            }
        }
        
        # Universal quick wins applicable to all businesses
        self.universal_quick_wins = [
            {
                'title': 'Power Factor Correction',
                'description': 'Install capacitor banks to improve power factor and reduce penalties',
                'impact': '5-10% reduction'
            },
            {
                'title': 'Plug Phantom Loads',
                'description': 'Unplug equipment when not in use to eliminate standby power consumption',
                'impact': '3-8% reduction'
            },
            {
                'title': 'Regular Maintenance',
                'description': 'Schedule preventive maintenance to keep equipment running efficiently',
                'impact': '5-12% reduction'
            }
        ]
    
    def get_suggestions(self, business_type, avg_emissions, current_reduction_pct):
        """
        Get personalized sustainability suggestions
        
        Args:
            business_type: Type of business
            avg_emissions: Average monthly emissions
            current_reduction_pct: Current reduction percentage vs baseline
        
        Returns:
            list: List of suggestion dictionaries
        """
        suggestions = []
        
        # Get industry-specific suggestions
        industry_suggestions = self.suggestions_db.get(business_type, self.suggestions_db['Manufacturing'])
        
        # Prioritize based on current performance
        if current_reduction_pct < 20:
            # Low performance - suggest high-impact changes
            priority_order = ['solar_power', 'energy_efficiency', 'refrigeration', 'hvac', 'server_efficiency']
        elif current_reduction_pct < 40:
            # Medium performance - balanced approach
            priority_order = ['lighting', 'water_heating', 'dryer_efficiency', 'waste_heat', 'power_management']
        else:
            # High performance - optimization
            priority_order = ['load_shifting', 'daylight', 'power_management']
        
        # Select top 3-5 suggestions
        for key in priority_order:
            if key in industry_suggestions:
                suggestions.append(industry_suggestions[key])
            if len(suggestions) >= 5:
                break
        
        # If not enough industry-specific suggestions, add from other industries
        if len(suggestions) < 3:
            for industry in self.suggestions_db.values():
                for suggestion in industry.values():
                    if suggestion not in suggestions:
                        suggestions.append(suggestion)
                        if len(suggestions) >= 5:
                            break
                if len(suggestions) >= 5:
                    break
        
        return suggestions[:5]
    
    def get_quick_wins(self, business_type):
        """
        Get quick win suggestions that can be implemented immediately
        
        Args:
            business_type: Type of business
        
        Returns:
            list: List of quick win suggestions
        """
        return self.universal_quick_wins
    
    def get_industry_benchmarks(self, business_type):
        """
        Get industry benchmark data for comparison
        
        Args:
            business_type: Type of business
        
        Returns:
            dict: Benchmark data
        """
        benchmarks = {
            'Manufacturing': {
                'industry_avg': 25.0,
                'top_performers': 45.0,
                'best_practice': 60.0
            },
            'Textile': {
                'industry_avg': 22.0,
                'top_performers': 42.0,
                'best_practice': 58.0
            },
            'Food Processing': {
                'industry_avg': 28.0,
                'top_performers': 48.0,
                'best_practice': 62.0
            },
            'Retail': {
                'industry_avg': 30.0,
                'top_performers': 50.0,
                'best_practice': 65.0
            },
            'Technology': {
                'industry_avg': 32.0,
                'top_performers': 52.0,
                'best_practice': 68.0
            }
        }
        
        return benchmarks.get(business_type, benchmarks['Manufacturing'])
    
    def generate_action_plan(self, suggestions, timeline_months=12):
        """
        Generate a phased implementation action plan
        
        Args:
            suggestions: List of suggestions
            timeline_months: Timeline for implementation
        
        Returns:
            dict: Phased action plan
        """
        # Sort by priority and payback period
        priority_order = {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        
        sorted_suggestions = sorted(
            suggestions,
            key=lambda x: (priority_order.get(x['priority'], 0), -self._get_payback_months(x['payback'])),
            reverse=True
        )
        
        # Create phases
        phase1 = []  # Month 1-3
        phase2 = []  # Month 4-6
        phase3 = []  # Month 7-12
        
        for suggestion in sorted_suggestions:
            if suggestion['priority'] in ['Very High', 'High']:
                if len(phase1) < 2:
                    phase1.append(suggestion)
                else:
                    phase2.append(suggestion)
            else:
                phase3.append(suggestion)
        
        return {
            'phase1': {'months': '1-3', 'actions': phase1},
            'phase2': {'months': '4-6', 'actions': phase2},
            'phase3': {'months': '7-12', 'actions': phase3}
        }
    
    def _get_payback_months(self, payback_str):
        """
        Convert payback period string to months
        
        Args:
            payback_str: Payback period string (e.g., "2-3 years")
        
        Returns:
            int: Approximate months
        """
        if 'month' in payback_str:
            return int(payback_str.split('-')[0].split()[0])
        elif 'year' in payback_str:
            years = int(payback_str.split('-')[0].split()[0])
            return years * 12
        return 24  # Default 2 years
