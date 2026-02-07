"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { LoadingScreen } from "@/components/ui/Spinner";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function ChatPage() {
  const { isAuthenticated, isLoading, user, getToken } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoadingResponse, setIsLoadingResponse] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    router.push("/auth/signin");
    return <LoadingScreen message="Redirecting to sign in..." />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoadingResponse) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoadingResponse(true);

    try {
      // Get auth token
      const token = await getToken();
      console.log("Token retrieved:", token ? `${token.substring(0, 20)}...` : 'null');

      // Call chat API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue,
        }),
      });

      console.log("Response status:", response.status, "Status text:", response.statusText);

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.statusText}`);
      }

      const data = await response.json();

      // Add AI response to messages
      const aiMessage: Message = {
        id: data.message_id,
        role: "assistant",
        content: data.response,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);

      // Add error message to UI
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "Sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoadingResponse(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950 overflow-x-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none w-full">
        <div className="absolute -top-20 -right-10 w-72 h-72 sm:-top-32 sm:-right-16 sm:w-96 sm:h-96 md:-top-40 md:-right-20 md:w-[500px] md:h-[500px] lg:-top-48 lg:-right-24 lg:w-[600px] lg:h-[600px] bg-blue-200/20 dark:bg-blue-500/10 rounded-full mix-blend-multiply blur-xl sm:blur-2xl md:blur-3xl animate-pulse"></div>
        <div className="absolute top-1/4 -left-8 w-64 h-64 sm:top-1/3 sm:-left-12 sm:w-80 sm:h-80 md:top-1/3 md:-left-16 md:w-96 md:h-96 lg:top-1/3 lg:-left-20 lg:w-[500px] lg:h-[500px] bg-purple-200/20 dark:bg-purple-500/10 rounded-full mix-blend-multiply blur-xl sm:blur-2xl md:blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="w-full px-0 sm:px-1 md:px-2 lg:px-3 xl:px-4 2xl:px-6">
        <div className="mb-6 sm:mb-8 pt-4 sm:pt-6 w-full">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-6 mb-6 sm:mb-8 w-full">
            <div className="space-y-2 w-full">
              <div className="flex items-center gap-2 sm:gap-3 w-full">
                <a href="/dashboard" className="p-1.5 sm:p-2 rounded-lg sm:rounded-xl bg-gradient-to-br from-gray-600 to-gray-700 shadow-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                </a>
                <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent w-full">
                  AI Chat Assistant
                </h1>
              </div>
              <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-400 w-full">
                Interact with our AI assistant to manage your tasks naturally
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-col h-[calc(100vh-200px)] max-w-4xl mx-auto">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto mb-4 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm p-4 sm:p-6 max-h-[60vh]">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-4">
                <div className="mb-4 p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  Welcome to AI Chat!
                </h3>
                <p className="text-gray-600 dark:text-gray-400 max-w-md">
                  Start a conversation by typing a message below. You can ask me to create, update, or manage your tasks using natural language.
                </p>
                <div className="mt-4 text-sm text-gray-500 dark:text-gray-400">
                  <p>Try: "Add a task to buy groceries"</p>
                  <p>Or: "Show me my tasks"</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        message.role === "user"
                          ? "bg-blue-600 text-white rounded-br-none"
                          : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none"
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div
                        className={`text-xs mt-1 ${
                          message.role === "user" ? "text-blue-200" : "text-gray-500 dark:text-gray-400"
                        }`}
                      >
                        {new Date(message.timestamp).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoadingResponse && (
                  <div className="flex justify-start">
                    <div className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-2xl rounded-bl-none px-4 py-3 max-w-[80%]">
                      <div className="flex items-center">
                        <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full mr-1 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full mr-1 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        <div className="h-2 w-2 bg-gray-500 dark:bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '600ms' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input form */}
          <form onSubmit={handleSubmit} className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm p-4">
            <div className="flex gap-2">
              <Input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message here..."
                disabled={isLoadingResponse}
                className="flex-1 border-0 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 bg-transparent"
              />
              <Button
                type="submit"
                disabled={!inputValue.trim() || isLoadingResponse}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6"
              >
                {isLoadingResponse ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Sending...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    Send
                  </span>
                )}
              </Button>
            </div>
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
              Ask me to create, update, or manage your tasks using natural language
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}