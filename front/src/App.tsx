import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import remarkGfm from 'remark-gfm';
import Header from './components/Header';
import UserInput from './components/UserInput';

function App() {
  const [contents, setContents] = useState<string[]>([]);
  const [currentContent, setCurrentContent] = useState<string>('');

  const addContent = (content: string) => {
    setContents((prevContents) => [...prevContents, content]);
    fetchUserInput(content);
  };

  const fetchUserInput = async (userInput: string) => {
    const res = await fetch(
      `http://127.0.0.1:8000?question=${encodeURIComponent(userInput)}`,
      {
        method: 'POST',
      }
    );

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const reader = res.body!.getReader();
    const decoder = new TextDecoder('utf-8');

    let result = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log('done');
        setContents((prevContents) => [...prevContents, result]);
        setCurrentContent('');
        break;
      }
      const decodedValue = decoder.decode(value);
      console.log({ decodedValue });
      result += decodedValue;
      setCurrentContent((prevContent) => prevContent + decodedValue);
    }
  };

  return (
    <div className='w-full mx-auto my-0 flex flex-col items-center'>
      <Header />
      <div className='w-full border-2 rounded-md'>
        <div className='w-full h-[80lvh] flex flex-col overflow-y-auto'>
          <div className='m-3 p-4 rounded-lg bg-lime-500 text-start'>
            <div>안녕하세요. 무엇을 도와드릴까요?</div>
          </div>
          {contents.map((content, index) => (
            <div
              key={index}
              className='m-3 p-4 rounded-lg even:text-end even:bg-lime-100 odd:bg-lime-500 odd:text-start'
            >
              <div className='prose'>
                <ReactMarkdown
                  rehypePlugins={[rehypeHighlight]}
                  remarkPlugins={[remarkGfm]}
                >
                  {content}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          {currentContent && (
            <div className='m-3 p-4 rounded-lg bg-lime-500 text-start'>
              <div className='prose'>
                <ReactMarkdown
                  // rehypePlugins={[rehypeHighlight]}
                  remarkPlugins={[remarkGfm]}
                >
                  {currentContent}
                </ReactMarkdown>
              </div>
            </div>
          )}
        </div>
        <UserInput contentAddHandler={addContent} />
      </div>
    </div>
  );
}

export default App;
