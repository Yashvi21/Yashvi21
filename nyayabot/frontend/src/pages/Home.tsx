import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Scale, 
  MessageSquare, 
  Users, 
  FileText, 
  Shield, 
  Clock,
  CheckCircle,
  ArrowRight
} from 'lucide-react';

const Home: React.FC = () => {
  const { isAuthenticated, user } = useAuth();

  const features = [
    {
      icon: MessageSquare,
      title: 'AI Legal Assistant',
      description: 'Get instant legal advice from our AI-powered chatbot trained on Indian law',
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      icon: Users,
      title: 'Verified Lawyers',
      description: 'Connect with qualified and verified lawyers across different specializations',
      color: 'text-green-600 dark:text-green-400'
    },
    {
      icon: FileText,
      title: 'Document Analysis',
      description: 'Upload legal documents for AI-powered analysis and summarization',
      color: 'text-purple-600 dark:text-purple-400'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your data is encrypted and protected with enterprise-grade security',
      color: 'text-red-600 dark:text-red-400'
    },
    {
      icon: Clock,
      title: '24/7 Availability',
      description: 'Access legal assistance anytime, anywhere with our round-the-clock service',
      color: 'text-yellow-600 dark:text-yellow-400'
    },
    {
      icon: CheckCircle,
      title: 'Easy Appointments',
      description: 'Schedule consultations with lawyers seamlessly through our platform',
      color: 'text-indigo-600 dark:text-indigo-400'
    }
  ];

  const legalCategories = [
    'Family Law', 'Criminal Law', 'Property Law', 'Consumer Protection',
    'Cyber Law', 'Labour Law', 'Civil Law', 'Tax Law'
  ];

  return (
    <div className="bg-white dark:bg-gray-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Your AI-Powered
              <span className="block text-blue-600 dark:text-blue-400">Legal Assistant</span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Get instant legal guidance, connect with verified lawyers, and manage your legal 
              documents all in one secure platform. NyayaBot makes legal help accessible to everyone.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {isAuthenticated ? (
                <Link
                  to={user?.user_type === 'lawyer' ? '/lawyer-dashboard' : '/dashboard'}
                  className="inline-flex items-center px-8 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              ) : (
                <>
                  <Link
                    to="/register"
                    className="inline-flex items-center px-8 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
                  >
                    Get Started Free
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </Link>
                  <Link
                    to="/chat"
                    className="inline-flex items-center px-8 py-3 rounded-lg border-2 border-blue-600 text-blue-600 dark:text-blue-400 font-semibold hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
                  >
                    Try AI Chat
                    <MessageSquare className="ml-2 w-5 h-5" />
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 w-72 h-72 bg-blue-300 dark:bg-blue-600 rounded-full mix-blend-multiply dark:mix-blend-normal opacity-20 animate-pulse"></div>
          <div className="absolute top-0 right-1/4 w-72 h-72 bg-purple-300 dark:bg-purple-600 rounded-full mix-blend-multiply dark:mix-blend-normal opacity-20 animate-pulse delay-1000"></div>
          <div className="absolute bottom-0 left-1/3 w-72 h-72 bg-pink-300 dark:bg-pink-600 rounded-full mix-blend-multiply dark:mix-blend-normal opacity-20 animate-pulse delay-2000"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose NyayaBot?
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              We combine cutting-edge AI technology with human expertise to provide 
              comprehensive legal assistance that's accessible, affordable, and reliable.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow"
              >
                <feature.icon className={`w-12 h-12 ${feature.color} mb-4`} />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Legal Categories Section */}
      <section className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Legal Expertise Across All Areas
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Our platform covers all major areas of Indian law with specialized 
              AI assistance and expert lawyers for each domain.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {legalCategories.map((category, index) => (
              <div
                key={index}
                className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg text-center hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <span className="text-gray-900 dark:text-white font-medium">
                  {category}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-blue-600 dark:bg-blue-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Get Legal Help?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of users who trust NyayaBot for their legal needs. 
            Start with a free consultation today.
          </p>
          
          {!isAuthenticated && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="inline-flex items-center px-8 py-3 rounded-lg bg-white text-blue-600 font-semibold hover:bg-gray-100 transition-colors"
              >
                Sign Up Now
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/lawyers"
                className="inline-flex items-center px-8 py-3 rounded-lg border-2 border-white text-white font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                Browse Lawyers
                <Users className="ml-2 w-5 h-5" />
              </Link>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;