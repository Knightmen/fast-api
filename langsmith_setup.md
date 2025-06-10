# LangSmith Integration Setup

## Overview
This FastAPI application now includes LangSmith monitoring to track tokens, resources, and LLM performance.

## Environment Variables Required

Add these variables to your `.env` file:

```bash
# LangSmith Configuration for monitoring tokens and resources
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=fastapi-chat-app
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

## Getting Your LangSmith API Key

1. Go to [LangSmith](https://smith.langchain.com/)
2. Sign up or log in to your account
3. Navigate to Settings → API Keys
4. Create a new API key and copy it
5. Add it to your `.env` file as `LANGCHAIN_API_KEY`

## What's Being Monitored

- **Token Usage**: Track input/output tokens for each LLM call
- **Response Times**: Monitor latency of each chat interaction
- **Error Rates**: Track failed requests and their causes
- **Session Tracking**: Monitor conversations by session ID
- **Resource Usage**: Monitor compute and memory usage

## New Endpoints

- `GET /langsmith/status` - Check LangSmith configuration status
- Updated `POST /session/chat` - Now includes monitoring data

## Usage

Once configured, all LLM interactions will automatically be logged to LangSmith. You can view:

1. **Traces**: Individual LLM calls with timing and token usage
2. **Sessions**: Conversation flows and user interactions
3. **Analytics**: Performance metrics and usage patterns
4. **Debugging**: Error logs and troubleshooting information

## Monitoring Dashboard

Visit your LangSmith dashboard at https://smith.langchain.com/ to view:
- Real-time traces
- Token usage analytics
- Performance metrics
- Error monitoring
- Usage trends

## Benefits

- **Cost Optimization**: Track token usage to optimize costs
- **Performance Monitoring**: Identify slow queries and bottlenecks
- **Quality Assurance**: Monitor response quality and user satisfaction
- **Debugging**: Quick identification and resolution of issues
- **Analytics**: Usage patterns and user behavior insights 