import Dashboard from "views/Dashboard.js";
import SentimentView from "views/SentimentView.js";

const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Summary",
    icon: "nc-icon nc-chart-pie-35",
    component: Dashboard,
    layout: "/admin",
  },
  {
    path: "/sentiment-analysis",
    name: "Daily Sentiment",
    icon: "nc-icon nc-bulb-63",
    component: SentimentView,
    layout: "/admin",
  },
  {
    path: "/historic-data",
    name: "Historic data",
    icon: "nc-icon nc-bulb-63",
    component: SentimentView,
    layout: "/admin",
  },
];

export default dashboardRoutes;
