"""Script to generate presentation slides."""
from site import abs_paths
import pandas as pd
from src.utils.presentation_generator import PresentationGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize presentation generator
        presentation = PresentationGenerator()
        
        # Slide 1: Project Overview
        presentation.add_title_slide(
            "TellCo Telecom Analysis",
            "Interim Findings"
        )
        
        # Slide 2: Key Findings
        presentation.add_bullet_slide(
            "Key Findings and Growth Opportunities",
            [
                "High-end smartphones dominate usage",
                "Social media and video streaming drive engagement",
                "Gaming apps show growing usage",
                "Premium users are key demographic for growth",
                "Network optimization opportunities identified"
            ]
        )
        
        # Slide 3: Handset Analysis
        presentation.add_bullet_slide(
            "Device Preferences",
            [
                "Top handsets dominated by premium devices",
                "Apple leads manufacturer market share",
                "High-end devices show increased data usage",
                "Opportunity for targeted premium services"
            ]
        )
        
        # Slide 4: User Engagement
        presentation.add_bullet_slide(
            "User Engagement Insights",
            [
                "Peak usage patterns identified in evening hours",
                "Social media drives majority of traffic",
                "Video streaming shows high engagement",
                "Gaming emerges as growth segment"
            ]
        )
        
        # Slide 5: Recommendations
        presentation.add_bullet_slide(
            "Recommendations",
            [
                "Focus on premium smartphone users",
                "Optimize network for video streaming",
                "Partner with top manufacturers",
                "Develop targeted marketing campaigns",
                "Implement user segmentation strategies"
            ]
        )
        
        # Slide 8: Experience Analysis Overview
        presentation.add_bullet_slide(
            "User Experience Analysis",
            [
                "Analysis of TCP retransmission rates",
                "Round Trip Time (RTT) patterns",
                "Throughput analysis by handset type",
                "Experience-based user segmentation"
            ]
        )
        
        # Slide 9: Throughput Analysis
        presentation.add_image_slide(
            "Throughput Analysis by Handset",
            abs_paths['throughput_handset'],
            [
                "Premium devices show higher throughput",
                "Significant variation across handset types",
                "Network optimization opportunities identified",
                "Device-specific performance patterns"
            ]
        )
        
        # Slide 10: TCP Retransmission Analysis
        presentation.add_image_slide(
            "TCP Retransmission Analysis",
            abs_paths['tcp_analysis'],
            [
                "TCP retransmission patterns vary by device",
                "Network congestion indicators identified",
                "Performance optimization needed for specific segments",
                "Impact on user experience quantified"
            ]
        )
        
        # Slide 11: Experience Clusters
        presentation.add_image_slide(
            "User Experience Segments",
            abs_paths['experience_clusters'],
            [
                "Three distinct experience segments identified",
                "Clear correlation with device types",
                "Network performance varies by segment",
                "Targeted improvement opportunities"
            ]
        )
        
        # Save presentation
        presentation.save("TellCo_Analysis_Interim.pptx")
        logger.info("Presentation generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 