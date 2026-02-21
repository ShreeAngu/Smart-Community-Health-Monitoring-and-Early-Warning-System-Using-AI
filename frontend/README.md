# Water-Borne Disease Prediction Frontend

React frontend application built with Vite, TypeScript, and Tailwind CSS for the Water-Borne Disease Prediction system.

## Features

- **Authentication**: JWT-based login with role-based access control
- **Role-based Dashboards**: Separate interfaces for Community users and Admins
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Real-time Data**: Integration with FastAPI backend for live predictions and alerts
- **Interactive Charts**: Data visualization using Recharts
- **Map Integration**: Leaflet maps for geographical data visualization

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Router DOM** for navigation
- **Axios** for API calls
- **Recharts** for data visualization
- **Leaflet** for maps
- **Lucide React** for icons

## Quick Start

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── PrivateRoute.tsx # Route protection component
├── context/            # React Context providers
│   └── AuthContext.tsx # Authentication state management
├── pages/              # Page components
│   ├── Login.tsx       # Login page
│   ├── CommunityDashboard.tsx  # Community user dashboard
│   └── AdminDashboard.tsx      # Admin dashboard
├── services/           # API service layer
│   └── api.ts          # Axios configuration and API calls
├── App.tsx             # Main app component with routing
├── main.tsx            # Application entry point
└── index.css           # Global styles with Tailwind
```

## Authentication

The app uses JWT tokens for authentication with two user roles:

### Community Users
- Submit health reports
- View personal predictions
- Check regional risk levels
- Receive alerts

### Admin Users
- View all system data
- Monitor regional risk assessments
- Manage alerts
- Access ML model insights
- View feature importance data

## Demo Credentials

- **Email**: test@example.com
- **Password**: testpassword123
- **Role**: Community (can be changed to admin in backend)

## API Integration

The frontend integrates with the FastAPI backend through:

- **Authentication**: `/login`, `/register`
- **Reports**: `/submit-report`, `/reports`
- **Predictions**: `/predict-risk`, `/predictions`
- **Regional Risk**: `/regional-risk`
- **Alerts**: `/alerts`
- **Dashboard**: `/dashboard`
- **Feature Importance**: `/feature-importance`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

Create a `.env` file for configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Deployment

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Deploy the `dist` folder** to your hosting service

## Features to Implement

- [ ] Report submission form
- [ ] Interactive maps with Leaflet
- [ ] Data visualization charts
- [ ] Real-time notifications
- [ ] Export functionality
- [ ] Advanced filtering and search
- [ ] Mobile app support

## Contributing

1. Follow TypeScript best practices
2. Use Tailwind CSS for styling
3. Implement proper error handling
4. Add loading states for async operations
5. Ensure responsive design
6. Write meaningful commit messages