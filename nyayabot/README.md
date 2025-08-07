# NyayaBot - AI-Powered Legal Assistant

NyayaBot is a comprehensive full-stack legal assistant web application that combines AI-powered legal guidance with human expertise from verified lawyers. The platform serves both general users seeking legal help and professional lawyers providing their services.

## 🌟 Features

### For General Users
- **AI Legal Assistant**: Get instant legal advice powered by OpenAI, trained on Indian law
- **Chat History**: View and manage previous AI conversations
- **Document Upload & Analysis**: Upload legal documents for AI-powered analysis and summarization
- **Lawyer Discovery**: Browse and connect with verified lawyers across different specializations
- **Direct Messaging**: Communicate directly with selected lawyers
- **Appointment Booking**: Schedule consultations with lawyers
- **Legal Awareness**: Access legal information, FAQs, and government schemes

### For Lawyers
- **Profile Management**: Create comprehensive profiles with specializations, experience, and credentials
- **Admin Approval System**: Secure verification process before platform access
- **Client Queries**: View and respond to user questions with AI-generated summaries
- **Appointment Management**: Set availability, approve/reschedule appointments
- **Document Review**: Access user-shared documents for consultation
- **Real-time Notifications**: Get notified of new messages and appointment requests
- **Rating System**: Build credibility through user feedback and ratings

### Technical Features
- **Role-based Authentication**: Secure token-based auth with user type management
- **Dark/Light Theme**: Seamless theme switching across the application
- **Responsive Design**: Mobile-first, accessible UI design
- **Real-time Updates**: Live notifications and messaging
- **Secure File Storage**: Document uploads via Cloudinary/AWS S3
- **RESTful APIs**: Comprehensive backend API with Django REST Framework

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7**: Python web framework
- **Django REST Framework**: API development
- **PostgreSQL/SQLite**: Database (configurable)
- **OpenAI API**: AI-powered legal assistance
- **Cloudinary**: File storage and management
- **Redis**: Caching and real-time features
- **Celery**: Background task processing

### Frontend
- **React 18**: Modern React with TypeScript
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Modern icon library
- **Axios**: HTTP client for API calls
- **Context API**: State management for auth and theme

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nyayabot/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd nyayabot/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - SQLite by default)
DATABASE_URL=postgresql://username:password@localhost:5432/nyayabot

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
```

## 📊 Database Schema

### Key Models

#### Authentication
- **User**: Custom user model with role-based access (user/lawyer/admin)
- **UserProfile**: Extended user information and preferences

#### Lawyers
- **LawyerProfile**: Professional information, specializations, verification status
- **LawyerRating**: User ratings and reviews for lawyers

#### Chat & Messaging
- **ChatSession**: AI chat sessions with users
- **ChatMessage**: Individual messages in AI conversations
- **LawyerUserConversation**: Direct messaging between users and lawyers
- **AIResponse**: Analytics and improvement tracking for AI responses

#### Documents & Appointments
- **Document**: File uploads with AI analysis capabilities
- **DocumentAnalysis**: Detailed AI-powered document analysis
- **Appointment**: Consultation scheduling system
- **AppointmentFeedback**: Post-consultation feedback system

## 🎨 UI/UX Design

### Design Principles
- **Minimalist**: Clean, distraction-free interface
- **Accessible**: WCAG compliant with proper contrast and navigation
- **Responsive**: Mobile-first design that works on all devices
- **Consistent**: Unified design system across all components

### Theme System
- **Light Mode**: Clean white interface with blue accents
- **Dark Mode**: Modern dark interface with proper contrast
- **System Sync**: Automatically follows system preferences
- **Persistent**: User preference saved across sessions

## 🔒 Security Features

- **Token-based Authentication**: Secure JWT-like token system
- **Role-based Access Control**: Different permissions for users/lawyers/admins
- **Input Validation**: Comprehensive form validation and sanitization
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **File Upload Security**: Secure file handling with type validation
- **Data Encryption**: Sensitive data protection in transit and at rest

## 📱 Mobile Support

The application is fully responsive and provides:
- **Mobile Navigation**: Collapsible hamburger menu
- **Touch-friendly**: Optimized tap targets and gestures
- **Progressive Web App**: Installable on mobile devices
- **Offline Capabilities**: Basic functionality without internet (planned)

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📈 Performance Optimization

- **Code Splitting**: React lazy loading for route-based splitting
- **Image Optimization**: Cloudinary automatic optimization
- **Caching**: Redis caching for frequently accessed data
- **Database Optimization**: Efficient queries with proper indexing
- **Bundle Optimization**: Webpack optimization for production builds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- The Django and React communities
- Indian legal professionals who provided domain expertise
- All contributors and testers

## 📞 Support

For support, email support@nyayabot.com or join our Discord server.

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Video consultation integration
- [ ] Mobile applications (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced AI legal research
- [ ] Payment gateway integration

### Version 1.2 (Future)
- [ ] Blockchain-based contract verification
- [ ] Integration with court systems
- [ ] Legal document templates
- [ ] Analytics dashboard for lawyers
- [ ] API for third-party integrations

---

Built with ❤️ for the Indian legal community