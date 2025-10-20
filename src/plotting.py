"""
Plotting Module
===============

This module provides visualization functions for the ML trading strategy.

Plots:
------
- Cumulative returns comparison (strategy vs benchmark)
- Predictions vs actual values
- Portfolio allocation over time
- Confusion matrix
- Drawdown chart
- Feature importance
- Training history

Functions:
---------
- plot_cumulative_returns: Plot strategy vs benchmark performance
- plot_predictions: Plot model predictions vs actual
- plot_portfolio_allocation: Plot portfolio weights over time
- plot_confusion_matrix: Plot confusion matrix
- plot_drawdown: Plot drawdown chart
- plot_feature_importance: Plot feature importance
- plot_training_history: Plot model training history
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging

# Configure plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StrategyVisualizer:
    """
    Visualization class for trading strategy analysis.
    """

    def __init__(self, config):
        """
        Initialize StrategyVisualizer.

        Parameters:
        -----------
        config : module
            Configuration module
        """
        self.config = config
        self.figure_size = config.FIGURE_SIZE
        self.dpi = config.DPI

    def plot_cumulative_returns(self, strategy_returns, benchmark_returns, save_path=None):
        """
        Plot cumulative returns comparison.

        Parameters:
        -----------
        strategy_returns : pd.Series
            Strategy returns
        benchmark_returns : pd.Series
            Benchmark returns
        save_path : str
            Path to save figure
        """
        logger.info("Plotting cumulative returns...")

        # Calculate cumulative returns
        strategy_cumulative = (1 + strategy_returns).cumprod()
        benchmark_cumulative = (1 + benchmark_returns).cumprod()

        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Plot
        ax.plot(strategy_cumulative.index, strategy_cumulative.values,
                label='ML Strategy', linewidth=2, color='#2E86AB')
        ax.plot(benchmark_cumulative.index, benchmark_cumulative.values,
                label='Buy & Hold (S&P 500)', linewidth=2, color='#A23B72', linestyle='--')

        # Formatting
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Return', fontsize=12, fontweight='bold')
        ax.set_title('Strategy Performance: Cumulative Returns', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)

        # Add horizontal line at y=1
        ax.axhline(y=1, color='black', linestyle='-', linewidth=0.5, alpha=0.5)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved cumulative returns plot to {save_path}")

        plt.close()

    def plot_predictions(self, dates, y_true, y_pred, y_proba=None, save_path=None):
        """
        Plot predictions vs actual values.

        Parameters:
        -----------
        dates : array-like
            Dates
        y_true : array-like
            True labels
        y_pred : array-like
            Predicted labels
        y_proba : array-like
            Prediction probabilities
        save_path : str
            Path to save figure
        """
        logger.info("Plotting predictions vs actual...")

        fig, axes = plt.subplots(2, 1, figsize=(self.figure_size[0], self.figure_size[1]*1.2), dpi=self.dpi)

        # Plot 1: Predictions vs Actual
        ax1 = axes[0]
        ax1.scatter(dates, y_true, label='Actual', alpha=0.6, s=20, color='#2E86AB')
        ax1.scatter(dates, y_pred, label='Predicted', alpha=0.6, s=20, color='#F18F01', marker='x')
        ax1.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Direction (0=Down, 1=Up)', fontsize=11, fontweight='bold')
        ax1.set_title('Model Predictions vs Actual Direction', fontsize=13, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Prediction Probabilities
        if y_proba is not None:
            ax2 = axes[1]
            colors = ['#A23B72' if pred == 0 else '#06A77D' for pred in y_pred]
            ax2.scatter(dates, y_proba, c=colors, alpha=0.6, s=20)
            ax2.axhline(y=0.5, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Decision Threshold')
            ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
            ax2.set_ylabel('Probability (Up)', fontsize=11, fontweight='bold')
            ax2.set_title('Prediction Probabilities', fontsize=13, fontweight='bold')
            ax2.legend(loc='best', fontsize=10)
            ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved predictions plot to {save_path}")

        plt.close()

    def plot_portfolio_allocation(self, weights_df, save_path=None):
        """
        Plot portfolio allocation over time.

        Parameters:
        -----------
        weights_df : pd.DataFrame
            Portfolio weights over time
        save_path : str
            Path to save figure
        """
        logger.info("Plotting portfolio allocation...")

        # Remove date column if present
        if 'date' in weights_df.columns:
            dates = weights_df['date']
            weights_df = weights_df.drop('date', axis=1)
        else:
            dates = weights_df.index

        # Create stacked area chart
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Plot stacked area
        ax.stackplot(dates, weights_df.T.values, labels=weights_df.columns, alpha=0.8)

        # Formatting
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Portfolio Weight', fontsize=12, fontweight='bold')
        ax.set_title('Portfolio Allocation Over Time', fontsize=14, fontweight='bold')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1])

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved allocation plot to {save_path}")

        plt.close()

    def plot_confusion_matrix(self, y_true, y_pred, save_path=None):
        """
        Plot confusion matrix.

        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred : array-like
            Predicted labels
        save_path : str
            Path to save figure
        """
        logger.info("Plotting confusion matrix...")

        from sklearn.metrics import confusion_matrix

        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred)

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6), dpi=self.dpi)

        # Plot heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                    xticklabels=['Down', 'Up'], yticklabels=['Down', 'Up'],
                    ax=ax, annot_kws={'size': 14, 'weight': 'bold'})

        # Formatting
        ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
        ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
        ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved confusion matrix to {save_path}")

        plt.close()

    def plot_drawdown(self, returns, save_path=None):
        """
        Plot drawdown chart.

        Parameters:
        -----------
        returns : pd.Series
            Returns
        save_path : str
            Path to save figure
        """
        logger.info("Plotting drawdown chart...")

        # Calculate cumulative returns and drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        # Create figure
        fig, axes = plt.subplots(2, 1, figsize=(self.figure_size[0], self.figure_size[1]*1.2), dpi=self.dpi)

        # Plot 1: Cumulative returns
        ax1 = axes[0]
        ax1.plot(cumulative.index, cumulative.values, linewidth=2, color='#2E86AB')
        ax1.plot(running_max.index, running_max.values, linewidth=1, linestyle='--',
                 color='#A23B72', alpha=0.7, label='Peak')
        ax1.set_ylabel('Cumulative Return', fontsize=11, fontweight='bold')
        ax1.set_title('Cumulative Returns and Drawdown', fontsize=13, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Drawdown
        ax2 = axes[1]
        ax2.fill_between(drawdown.index, drawdown.values, 0, color='#E63946', alpha=0.6)
        ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Drawdown', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Format y-axis as percentage
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved drawdown chart to {save_path}")

        plt.close()

    def plot_training_history(self, history, save_path=None):
        """
        Plot model training history.

        Parameters:
        -----------
        history : keras.callbacks.History
            Training history
        save_path : str
            Path to save figure
        """
        logger.info("Plotting training history...")

        fig, axes = plt.subplots(2, 2, figsize=(self.figure_size[0], self.figure_size[1]), dpi=self.dpi)

        metrics = ['loss', 'accuracy', 'precision', 'auc']
        titles = ['Loss', 'Accuracy', 'Precision', 'AUC']

        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            if metric in history.history:
                ax.plot(history.history[metric], label='Train', linewidth=2)
                ax.plot(history.history[f'val_{metric}'], label='Validation', linewidth=2)
                ax.set_xlabel('Epoch', fontsize=10, fontweight='bold')
                ax.set_ylabel(title, fontsize=10, fontweight='bold')
                ax.set_title(f'Model {title}', fontsize=11, fontweight='bold')
                ax.legend(loc='best', fontsize=9)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved training history to {save_path}")

        plt.close()

    def plot_feature_importance(self, feature_importance, top_n=20, save_path=None):
        """
        Plot feature importance.

        Parameters:
        -----------
        feature_importance : pd.Series or dict
            Feature importance scores
        top_n : int
            Number of top features to display
        save_path : str
            Path to save figure
        """
        logger.info("Plotting feature importance...")

        if isinstance(feature_importance, dict):
            feature_importance = pd.Series(feature_importance)

        # Sort and select top N
        top_features = feature_importance.nlargest(top_n)

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        # Plot horizontal bar chart
        colors = sns.color_palette("viridis", len(top_features))
        top_features.sort_values().plot(kind='barh', ax=ax, color=colors)

        # Formatting
        ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Feature', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Feature Importance', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved feature importance plot to {save_path}")

        plt.close()

    def create_interactive_dashboard(self, results_df, save_path=None):
        """
        Create interactive dashboard with Plotly.

        Parameters:
        -----------
        results_df : pd.DataFrame
            Backtest results
        save_path : str
            Path to save HTML file
        """
        logger.info("Creating interactive dashboard...")

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Portfolio Value', 'Daily Returns', 'Position Status', 'Cumulative Return'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )

        # Plot 1: Portfolio value
        fig.add_trace(
            go.Scatter(x=results_df['date'], y=results_df['portfolio_value'],
                      name='Portfolio Value', line=dict(color='#2E86AB', width=2)),
            row=1, col=1
        )

        # Plot 2: Daily returns
        fig.add_trace(
            go.Bar(x=results_df['date'], y=results_df['daily_return'],
                  name='Daily Return', marker_color='#F18F01'),
            row=1, col=2
        )

        # Plot 3: Position status
        fig.add_trace(
            go.Scatter(x=results_df['date'], y=results_df['in_market'],
                      name='In Market', fill='tozeroy', line=dict(color='#06A77D')),
            row=2, col=1
        )

        # Plot 4: Cumulative return
        fig.add_trace(
            go.Scatter(x=results_df['date'], y=results_df['cumulative_return'],
                      name='Cumulative Return', line=dict(color='#A23B72', width=2)),
            row=2, col=2
        )

        # Update layout
        fig.update_layout(
            title_text="Trading Strategy Dashboard",
            showlegend=True,
            height=800,
            template='plotly_white'
        )

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Saved interactive dashboard to {save_path}")

        return fig


if __name__ == "__main__":
    logger.info("Plotting module loaded successfully")
