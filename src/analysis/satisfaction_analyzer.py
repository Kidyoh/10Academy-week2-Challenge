"""User satisfaction analysis module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import logging
from typing import Dict, Tuple
from pathlib import Path

logger = logging.getLogger('tellco_analysis')

class SatisfactionAnalyzer:
    """Class for analyzing user satisfaction based on engagement and experience."""
    
    def __init__(self, engagement_data: pd.DataFrame, experience_data: pd.DataFrame):
        """Initialize with engagement and experience data."""
        self.engagement_data = engagement_data
        self.experience_data = experience_data
        self.satisfaction_scores = None
        
    def calculate_engagement_score(self) -> pd.DataFrame:
        """Calculate engagement score using Euclidean distance from least engaged cluster."""
        try:
            # Get features for engagement scoring
            features = ['session_count', 'total_duration', 'total_traffic']
            X = self.engagement_data[features].copy()
            
            # Normalize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Find least engaged cluster center
            kmeans = KMeans(n_clusters=3, random_state=42)
            kmeans.fit(X_scaled)
            least_engaged_center = kmeans.cluster_centers_[0]
            
            # Calculate Euclidean distance
            distances = np.sqrt(((X_scaled - least_engaged_center) ** 2).sum(axis=1))
            
            # Normalize scores to 0-1 range
            engagement_scores = (distances - distances.min()) / (distances.max() - distances.min())
            
            return pd.DataFrame({
                'msisdn': self.engagement_data['msisdn'],
                'engagement_score': engagement_scores
            })
        except Exception as e:
            logger.error(f"Error calculating engagement score: {str(e)}")
            raise
    
    def calculate_experience_score(self) -> pd.DataFrame:
        """Calculate experience score using Euclidean distance from worst experience cluster."""
        try:
            features = ['avg_tcp_retrans', 'avg_rtt', 'avg_throughput']
            X = self.experience_data[features].copy()
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=3, random_state=42)
            kmeans.fit(X_scaled)
            worst_experience_center = kmeans.cluster_centers_[2]
            
            distances = np.sqrt(((X_scaled - worst_experience_center) ** 2).sum(axis=1))
            experience_scores = (distances - distances.min()) / (distances.max() - distances.min())
            
            return pd.DataFrame({
                'msisdn': self.experience_data['msisdn'],
                'experience_score': experience_scores
            })
        except Exception as e:
            logger.error(f"Error calculating experience score: {str(e)}")
            raise
    
    def calculate_satisfaction_scores(self) -> pd.DataFrame:
        """Calculate overall satisfaction scores."""
        try:
            engagement_scores = self.calculate_engagement_score()
            experience_scores = self.calculate_experience_score()
            
            satisfaction = pd.merge(
                engagement_scores,
                experience_scores,
                on='msisdn',
                how='inner'
            )
            
            satisfaction['satisfaction_score'] = (
                satisfaction['engagement_score'] + satisfaction['experience_score']
            ) / 2
            
            self.satisfaction_scores = satisfaction
            return satisfaction
        except Exception as e:
            logger.error(f"Error calculating satisfaction scores: {str(e)}")
            raise
    
    def save_results(self, output_dir: str = "data/processed") -> Dict[str, str]:
        """Save analysis results to files."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save satisfaction scores
            scores_path = output_path / "satisfaction_scores.csv"
            self.satisfaction_scores.to_csv(scores_path, index=False)
            
            # Save cluster statistics if available
            if hasattr(self, 'cluster_stats'):
                stats_path = output_path / "satisfaction_clusters.csv"
                self.cluster_stats.to_csv(stats_path)
            
            logger.info(f"Results saved to {output_dir}")
            return {
                'satisfaction_scores': str(scores_path),
                'cluster_stats': str(stats_path) if hasattr(self, 'cluster_stats') else None
            }
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise
    
    def export_to_database(self, connection_string: str) -> bool:
        """Export results to database with error handling."""
        try:
            import sqlalchemy as sa
            engine = sa.create_engine(connection_string)
            
            if self.satisfaction_scores is None:
                self.calculate_satisfaction_scores()
            
            # Test connection before attempting export
            with engine.connect() as conn:
                self.satisfaction_scores.to_sql(
                    'user_satisfaction',
                    conn,
                    if_exists='replace',
                    index=False
                )
            
            logger.info("Successfully exported to database")
            return True
            
        except ImportError:
            logger.warning("SQLAlchemy not installed. Saving to CSV instead.")
            self.save_results()
            return False
            
        except Exception as e:
            logger.error(f"Database export failed: {str(e)}")
            logger.info("Falling back to CSV export")
            self.save_results()
            return False
    
    def get_top_satisfied_customers(self, n: int = 10) -> pd.DataFrame:
        """Get top n satisfied customers.
        
        Args:
            n (int): Number of top customers to return
            
        Returns:
            pd.DataFrame: Top n customers with their satisfaction scores
        """
        try:
            if self.satisfaction_scores is None:
                self.calculate_satisfaction_scores()
                
            top_customers = self.satisfaction_scores.nlargest(n, 'satisfaction_score')
            
            # Add engagement and experience details
            result = pd.merge(
                top_customers,
                self.engagement_data[['msisdn', 'session_count', 'total_duration', 'total_traffic']],
                on='msisdn',
                how='left'
            )
            
            result = pd.merge(
                result,
                self.experience_data[['msisdn', 'handset_type', 'avg_throughput']],
                on='msisdn',
                how='left'
            )
            
            # Format the results
            result = result[[
                'msisdn', 'satisfaction_score', 'engagement_score', 'experience_score',
                'session_count', 'total_duration', 'total_traffic',
                'handset_type', 'avg_throughput'
            ]].round(4)
            
            logger.info(f"Retrieved top {n} satisfied customers")
            return result
            
        except Exception as e:
            logger.error(f"Error getting top satisfied customers: {str(e)}")
            raise
    
    def build_satisfaction_model(self) -> Tuple[object, Dict]:
        """Build and evaluate regression model for satisfaction prediction."""
        try:
            if self.satisfaction_scores is None:
                self.calculate_satisfaction_scores()
                
            # Prepare features
            features = pd.merge(
                self.engagement_data,
                self.experience_data,
                on='msisdn',
                how='inner'
            )
            
            X = features[[
                'session_count', 'total_duration', 'total_traffic',
                'avg_tcp_retrans', 'avg_rtt', 'avg_throughput'
            ]]
            y = self.satisfaction_scores['satisfaction_score']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred)
            }
            
            logger.info("Satisfaction prediction model built successfully")
            return model, metrics
            
        except Exception as e:
            logger.error(f"Error building satisfaction model: {str(e)}")
            raise
    
    def cluster_satisfaction_scores(self, k: int = 2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Perform k-means clustering on satisfaction scores."""
        try:
            if self.satisfaction_scores is None:
                self.calculate_satisfaction_scores()
                
            # Prepare features for clustering
            X = self.satisfaction_scores[['engagement_score', 'experience_score']]
            
            # Perform clustering
            kmeans = KMeans(n_clusters=k, random_state=42)
            self.satisfaction_scores['satisfaction_cluster'] = kmeans.fit_predict(X)
            
            # Calculate cluster statistics
            cluster_stats = self.satisfaction_scores.groupby('satisfaction_cluster').agg({
                'satisfaction_score': ['mean', 'std', 'count'],
                'engagement_score': 'mean',
                'experience_score': 'mean'
            }).round(4)
            
            # Add cluster descriptions
            descriptions = {
                0: "Less Satisfied: Lower engagement and experience scores",
                1: "More Satisfied: Higher engagement and experience scores"
            }
            
            cluster_stats['description'] = cluster_stats.index.map(descriptions)
            self.cluster_stats = cluster_stats
            
            logger.info(f"Clustered users into {k} satisfaction groups")
            return self.satisfaction_scores, cluster_stats
            
        except Exception as e:
            logger.error(f"Error clustering satisfaction scores: {str(e)}")
            raise