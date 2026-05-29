import { useState } from "react"
import axios from "axios"
import ReactMarkdown from "react-markdown"

function App() {

  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const [lectureName, setLectureName] = useState("")
  const [summaryLoading, setSummaryLoading] = useState(false)
  const [summaryResult, setSummaryResult] = useState(null)

  async function searchLecture() {

    if (!query) return

    try {

      setLoading(true)

      const response = await axios.get(
        "http://127.0.0.1:8000/search",
        {
          params: {
            query: query
          }
        }
      )

      console.log(response.data)

      setResult(response.data)

    } catch (error) {

      console.log(error)

    } finally {

      setLoading(false)

    }

  }

  async function getSummary() {

    if (!lectureName) return

    try {

      setSummaryLoading(true)

      const response = await axios.get(
        "http://127.0.0.1:8000/summary",
        {
          params: {
            lecture: lectureName
          }
        }
      )

      console.log(response.data)

      setSummaryResult(response.data)

    } catch (error) {

      console.log(error)

    } finally {

      setSummaryLoading(false)

    }

  }

  return (

    <div className="min-h-screen bg-[#020817] text-white px-6 py-10">

      <div className="max-w-5xl mx-auto">

        <div className="flex items-center gap-4 mb-12">

          <img
            src="https://upload.wikimedia.org/wikipedia/en/1/12/IIT_Guwahati_Logo.svg"
            alt="IIT Guwahati"
            className="w-16 h-16"
          />

          <div>

            <h1 className="text-4xl font-bold">
              AI Lecture Assistant
            </h1>

            <p className="text-zinc-400 mt-1 text-lg">
              IIT Guwahati • Applied Machine Learning for Signal Processing
            </p>

          </div>

        </div>

        <div className="bg-[#0f172a] border border-white/10 rounded-3xl p-6 shadow-2xl">

          <h2 className="text-2xl font-bold mb-5">
            Search Lecture
          </h2>

          <input
            type="text"
            placeholder="Ask about FFT, EEG, ECG, Pitch Estimation..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-[#1e293b] border border-white/10 rounded-2xl px-5 py-4 outline-none text-lg"
          />

          <button
            onClick={searchLecture}
            className="mt-5 bg-blue-500 hover:bg-blue-600 transition px-6 py-3 rounded-2xl font-semibold cursor-pointer"
          >

            {
              loading
                ? "Searching..."
                : "Search Lecture"
            }

          </button>

        </div>

        {
          result && (

            <div className="mt-8 bg-[#0f172a] border border-white/10 rounded-3xl p-6">

              <div className="flex items-center justify-between mb-6">

                <h2 className="text-2xl font-bold">
                  AI Response
                </h2>

                <div className="bg-blue-500/10 text-blue-300 px-4 py-2 rounded-xl text-sm">

                  Confidence • {result.confidence}%

                </div>

              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-6">

                <div className="bg-[#1e293b] rounded-2xl p-5">

                  <h3 className="text-blue-300 font-semibold mb-2 text-lg">
                    Lecture
                  </h3>

                  <p className="text-zinc-300">
                    {result.lecture}
                  </p>

                </div>

                <div className="bg-[#1e293b] rounded-2xl p-5">

                  <h3 className="text-cyan-300 font-semibold mb-2 text-lg">
                    Timestamp
                  </h3>

                  <p className="text-zinc-300">
                    {result.start} → {result.end}
                  </p>

                </div>

              </div>

              <div className="bg-[#1e293b] rounded-2xl p-5">

                <h3 className="text-indigo-300 font-semibold mb-4 text-2xl">
                  Explanation
                </h3>

                <div className="text-zinc-300 leading-8 prose prose-invert max-w-none">

                  <ReactMarkdown>
                    {result.answer}
                  </ReactMarkdown>

                </div>

              </div>

            </div>

          )
        }

        <div className="mt-10 bg-[#0f172a] border border-white/10 rounded-3xl p-6 shadow-2xl">

          <h2 className="text-2xl font-bold mb-5">
            Lecture Summary
          </h2>

          <input
            type="text"
            placeholder="Example: ECG_EEG_and_Brain_Signals"
            value={lectureName}
            onChange={(e) => setLectureName(e.target.value)}
            className="w-full bg-[#1e293b] border border-white/10 rounded-2xl px-5 py-4 outline-none text-lg"
          />

          <button
            onClick={getSummary}
            className="mt-5 bg-cyan-500 hover:bg-cyan-600 transition px-6 py-3 rounded-2xl font-semibold cursor-pointer"
          >

            {
              summaryLoading
                ? "Loading..."
                : "Get Summary"
            }

          </button>

        </div>

        {
          summaryResult && (

            <div className="mt-8 bg-[#0f172a] border border-white/10 rounded-3xl p-6">

              <h2 className="text-2xl font-bold mb-6">
                Lecture Summary
              </h2>

              <div className="bg-[#1e293b] rounded-2xl p-6">

                <div className="text-zinc-300 leading-8 prose prose-invert max-w-none">

                  <ReactMarkdown>
                    {summaryResult.summary}
                  </ReactMarkdown>

                </div>

              </div>

            </div>

          )
        }

      </div>

    </div>

  )
}

export default App