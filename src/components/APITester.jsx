import React, { useState, useEffect } from 'react';
import { ChevronDown, Play, Copy, AlertCircle, CheckCircle, Loader } from 'lucide-react';

export default function APITester() {
  const [openAPI, setOpenAPI] = useState(null);
  const [selectedTag, setSelectedTag] = useState('Users');
  const [selectedEndpoint, setSelectedEndpoint] = useState(null);
  const [testParams, setTestParams] = useState({});
  const [testBody, setTestBody] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const API_BASE = 'http://localhost:8000';

  // OpenAPI 명세 가져오기
  useEffect(() => {
    const fetchOpenAPI = async () => {
      try {
        const res = await fetch(`${API_BASE}/openapi.json`);
        const data = await res.json();
        setOpenAPI(data);
      } catch (err) {
        console.error('Failed to fetch OpenAPI spec:', err);
      }
    };
    fetchOpenAPI();
  }, []);

  if (!openAPI) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-center">
          <Loader className="animate-spin mx-auto mb-4" size={40} />
          <p>API 명세 로딩 중...</p>
          <p className="text-sm text-slate-400 mt-2">http://localhost:8000에서 API 서버를 실행하세요</p>
        </div>
      </div>
    );
  }

  const paths = openAPI.paths || {};
  const tags = Object.keys(openAPI.tags?.reduce((acc, tag) => ({...acc, [tag.name]: true}), {}) || {});
  const endpoints = Object.entries(paths)
    .flatMap(([path, methods]) =>
      Object.entries(methods).map(([method, details]) => ({
        path,
        method: method.toUpperCase(),
        ...details
      }))
    )
    .filter(ep => ep.tags?.[0] === selectedTag);

  const handleTestClick = (endpoint) => {
    setSelectedEndpoint(endpoint);
    setTestParams({});
    setTestBody('');
    setResponse(null);
  };

  const handleParamChange = (paramName, value) => {
    setTestParams(prev => ({...prev, [paramName]: value}));
  };

  const executeRequest = async () => {
    if (!selectedEndpoint) return;

    setLoading(true);
    try {
      let url = `${API_BASE}${selectedEndpoint.path}`;
      
      // URL 경로 파라미터 치환
      if (selectedEndpoint.parameters) {
        selectedEndpoint.parameters.forEach(param => {
          if (param.in === 'path') {
            url = url.replace(`{${param.name}}`, testParams[param.name] || '');
          }
        });
      }

      // 쿼리 파라미터 추가
      const queryParams = new URLSearchParams();
      if (selectedEndpoint.parameters) {
        selectedEndpoint.parameters.forEach(param => {
          if (param.in === 'query' && testParams[param.name]) {
            queryParams.append(param.name, testParams[param.name]);
          }
        });
      }
      if (queryParams.toString()) {
        url += '?' + queryParams.toString();
      }

      const options = {
        method: selectedEndpoint.method,
        headers: { 'Content-Type': 'application/json' }
      };

      if (testBody && (selectedEndpoint.method === 'POST' || selectedEndpoint.method === 'PUT' || selectedEndpoint.method === 'PATCH')) {
        options.body = testBody;
      }

      const res = await fetch(url, options);
      const data = await res.json();
      
      setResponse({
        status: res.status,
        statusText: res.statusText,
        data,
        success: res.ok
      });
    } catch (err) {
      setResponse({
        status: 0,
        statusText: 'Error',
        data: { error: err.message },
        success: false
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getMethodColor = (method) => {
    const colors = {
      GET: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      POST: 'bg-green-500/20 text-green-300 border-green-500/30',
      PUT: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      PATCH: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      DELETE: 'bg-red-500/20 text-red-300 border-red-500/30'
    };
    return colors[method] || colors.GET;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-6">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Poppins:wght@600;700&display=swap');
        
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }
        
        .endpoint-card {
          background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
          border: 1px solid rgba(148, 163, 184, 0.2);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .endpoint-card:hover {
          border-color: rgba(148, 163, 184, 0.5);
          background: linear-gradient(135deg, rgba(30, 41, 59, 1), rgba(15, 23, 42, 1));
          transform: translateX(4px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .code-block {
          background: rgba(15, 23, 42, 0.9);
          border: 1px solid rgba(148, 163, 184, 0.2);
          border-radius: 8px;
          padding: 12px 14px;
          font-family: 'JetBrains Mono', monospace;
          font-size: 13px;
          overflow-x: auto;
        }
        
        .parameter-input {
          background: rgba(30, 41, 59, 0.6);
          border: 1px solid rgba(148, 163, 184, 0.3);
          border-radius: 6px;
          padding: 8px 12px;
          color: white;
          transition: all 0.2s;
        }
        
        .parameter-input:focus {
          outline: none;
          border-color: rgb(96, 165, 250);
          background: rgba(30, 41, 59, 0.9);
          box-shadow: 0 0 12px rgba(96, 165, 250, 0.2);
        }
        
        .btn-primary {
          background: linear-gradient(135deg, rgb(59, 130, 246), rgb(37, 99, 235));
          transition: all 0.3s;
        }
        
        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 24px rgba(59, 130, 246, 0.4);
        }
        
        .success-badge {
          background: rgba(34, 197, 94, 0.2);
          border: 1px solid rgb(34, 197, 94);
        }
        
        .error-badge {
          background: rgba(239, 68, 68, 0.2);
          border: 1px solid rgb(239, 68, 68);
        }
      `}</style>

      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
            API Tester
          </h1>
          <p className="text-slate-400">로컬 API 서버의 엔드포인트를 탐색하고 테스트합니다</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - Endpoints */}
          <div className="lg:col-span-1">
            <div className="sticky top-6">
              <h2 className="text-lg font-semibold mb-4 text-slate-300">태그</h2>
              <div className="space-y-2">
                {tags.map(tag => (
                  <button
                    key={tag}
                    onClick={() => setSelectedTag(tag)}
                    className={`w-full text-left px-4 py-2 rounded-lg transition ${
                      selectedTag === tag
                        ? 'bg-blue-500/20 border border-blue-400 text-blue-300'
                        : 'hover:bg-slate-700/50 text-slate-300'
                    }`}
                  >
                    {tag}
                  </button>
                ))}
              </div>

              <h2 className="text-lg font-semibold mt-8 mb-4 text-slate-300">엔드포인트</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {endpoints.map((ep, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleTestClick(ep)}
                    className={`endpoint-card w-full text-left px-3 py-2 rounded-lg border transition group ${
                      selectedEndpoint === ep ? 'bg-slate-600/50 border-slate-400' : ''
                    }`}
                  >
                    <div className={`inline-block px-2 py-1 rounded text-xs font-mono font-bold ${getMethodColor(ep.method)} border`}>
                      {ep.method}
                    </div>
                    <p className="text-sm text-slate-300 mt-1 truncate group-hover:text-slate-100">{ep.path}</p>
                    <p className="text-xs text-slate-500 mt-1">{ep.summary}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right Content - Test Panel */}
          <div className="lg:col-span-2 space-y-6">
            {selectedEndpoint ? (
              <>
                {/* Endpoint Details */}
                <div className="endpoint-card rounded-lg p-6 border">
                  <div className="flex items-center gap-3 mb-4">
                    <span className={`inline-block px-3 py-1 rounded-lg text-sm font-bold font-mono ${getMethodColor(selectedEndpoint.method)} border`}>
                      {selectedEndpoint.method}
                    </span>
                    <span className="text-slate-300 font-mono">{selectedEndpoint.path}</span>
                    <button
                      onClick={() => copyToClipboard(`${API_BASE}${selectedEndpoint.path}`)}
                      className="ml-auto p-2 hover:bg-slate-700 rounded transition"
                    >
                      <Copy size={16} />
                    </button>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{selectedEndpoint.summary}</h3>
                  {selectedEndpoint.description && (
                    <p className="text-slate-400 text-sm">{selectedEndpoint.description}</p>
                  )}
                </div>

                {/* Parameters */}
                {selectedEndpoint.parameters && selectedEndpoint.parameters.length > 0 && (
                  <div className="endpoint-card rounded-lg p-6 border">
                    <h3 className="font-semibold mb-4 flex items-center gap-2">
                      <span className="text-sm bg-blue-500/30 px-2 py-1 rounded text-blue-300">파라미터</span>
                      <span className="text-slate-500 text-sm">총 {selectedEndpoint.parameters.length}개</span>
                    </h3>
                    <div className="space-y-3">
                      {selectedEndpoint.parameters.map((param, idx) => (
                        <div key={idx}>
                          <label className="text-sm text-slate-400 mb-1 block">
                            {param.name}
                            {param.required && <span className="text-red-400">*</span>}
                            <span className="text-xs text-slate-600 ml-2">({param.in})</span>
                          </label>
                          <input
                            type="text"
                            placeholder={param.description}
                            value={testParams[param.name] || ''}
                            onChange={(e) => handleParamChange(param.name, e.target.value)}
                            className="parameter-input w-full"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Request Body */}
                {(selectedEndpoint.method === 'POST' || selectedEndpoint.method === 'PUT' || selectedEndpoint.method === 'PATCH') && (
                  <div className="endpoint-card rounded-lg p-6 border">
                    <h3 className="font-semibold mb-4 flex items-center gap-2">
                      <span className="text-sm bg-green-500/30 px-2 py-1 rounded text-green-300">요청 본문</span>
                    </h3>
                    <textarea
                      value={testBody}
                      onChange={(e) => setTestBody(e.target.value)}
                      placeholder='{"name": "John", "email": "john@example.com"}'
                      className="parameter-input w-full h-32 font-mono text-sm"
                    />
                  </div>
                )}

                {/* Execute Button */}
                <button
                  onClick={executeRequest}
                  disabled={loading}
                  className="btn-primary w-full py-3 rounded-lg font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  <Play size={18} />
                  {loading ? '실행 중...' : 'API 호출'}
                </button>

                {/* Response */}
                {response && (
                  <div className={`endpoint-card rounded-lg p-6 border ${response.success ? 'success-badge' : 'error-badge'}`}>
                    <div className="flex items-center gap-2 mb-4">
                      {response.success ? (
                        <CheckCircle size={20} className="text-green-400" />
                      ) : (
                        <AlertCircle size={20} className="text-red-400" />
                      )}
                      <span className="font-semibold">응답 ({response.status} {response.statusText})</span>
                      <button
                        onClick={() => copyToClipboard(JSON.stringify(response.data, null, 2))}
                        className="ml-auto p-2 hover:bg-slate-700 rounded transition"
                      >
                        <Copy size={16} />
                      </button>
                    </div>
                    <div className="code-block">
                      <pre className="text-green-400">{JSON.stringify(response.data, null, 2)}</pre>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="flex items-center justify-center h-96 text-slate-500">
                <div className="text-center">
                  <ChevronDown size={48} className="mx-auto mb-4 opacity-50" />
                  <p>왼쪽에서 엔드포인트를 선택하세요</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
