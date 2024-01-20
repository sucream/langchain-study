import { useState, KeyboardEvent } from 'react';

export default function UserInput({
  contentAddHandler,
}: {
  contentAddHandler: (content: string) => void;
}) {
  const [userInput, setUserInput] = useState<string>('');

  const handleOnKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      contentAddHandler(userInput);
      setUserInput('');
    }
  };

  return (
    <div className='flex m-2'>
      <input
        className='w-3/4 border-2 rounded-sm'
        type='text'
        placeholder='메시지를 입력하세요'
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyPress={handleOnKeyPress}
      />
      <button
        className='w-1/4 p-2 bg-blue-300 rounded-md'
        onClick={() => {
          contentAddHandler(userInput);
          setUserInput('');
        }}
      >
        전송
      </button>
    </div>
  );
}
