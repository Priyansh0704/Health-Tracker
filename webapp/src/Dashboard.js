import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import allChats from './data/all_chats.json';
import './Dashboard.css'; // We will create this CSS file next

// Register the components from Chart.js that we will be using
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

// --- Data Processing Function ---
const processChatData = () => {
  const monthlyMetrics = {
    January: { workout: 0, missed: 0, stress: 0 },
    February: { workout: 0, missed: 0, stress: 0 },
    March: { workout: 0, missed: 0, stress: 0 },
    April: { workout: 0, missed: 0, stress: 0 },
    May: { workout: 0, missed: 0, stress: 0 },
    June: { workout: 0, missed: 0, stress: 0 },
    July: { workout: 0, missed: 0, stress: 0 },
    August: { workout: 0, missed: 0, stress: 0 },
  };

  const teamEngagement = {};

  for (const chat of allChats) {
    // Process for Monthly Adherence & Stress
    const month = new Date(chat.ts).toLocaleString('default', { month: 'long' });
    if (monthlyMetrics[month]) {
      const text = chat.text.toLowerCase();
      if (text.includes('workout')) monthlyMetrics[month].workout++;
      if (text.includes('missed')) monthlyMetrics[month].missed++;
      if (text.includes('stress')) monthlyMetrics[month].stress++;
    }

    // Process for Team Engagement
    if (chat.role !== 'member') {
      teamEngagement[chat.sender] = (teamEngagement[chat.sender] || 0) + 1;
    }
  }

  return { monthlyMetrics, teamEngagement };
};

// --- Main Dashboard Component ---
const Dashboard = () => {
  const { monthlyMetrics, teamEngagement } = processChatData();

  // Data for the Bar Chart
  const adherenceChartData = {
    labels: Object.keys(monthlyMetrics),
    datasets: [
      {
        label: 'Workouts Completed',
        data: Object.values(monthlyMetrics).map(m => m.workout),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
      {
        label: 'Workouts Missed',
        data: Object.values(monthlyMetrics).map(m => m.missed),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
      {
        label: 'Mentions of Stress',
        data: Object.values(monthlyMetrics).map(m => m.stress),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
      },
    ],
  };

  // Data for the Pie Chart
  const engagementChartData = {
    labels: Object.keys(teamEngagement),
    datasets: [
      {
        label: '# of Messages',
        data: Object.values(teamEngagement),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="dashboard-container">
      <h1>Analytics Dashboard</h1>
      <div className="chart-wrapper">
        <h2 className="chart-title">Member Adherence & Stress Trends</h2>
        <Bar options={chartOptions} data={adherenceChartData} />
      </div>
      <div className="chart-wrapper">
        <h2 className="chart-title">Team Engagement Distribution</h2>
        <div className="pie-chart-container">
            <Pie options={chartOptions} data={engagementChartData} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;