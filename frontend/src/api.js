const API_BASE_URL = 'http://127.0.0.1:8000'

export async function analyzeRepository(owner, repo) {
  const response = await fetch(`${API_BASE_URL}/recon/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      owner,
      repo,
    }),
  })

  if (!response.ok) {
    let errorMessage =
      `The reconnaissance backend returned an error (${response.status}).`

    try {
      const errorData = await response.json()

      if (errorData.detail) {
        errorMessage = errorData.detail
      }
    } catch {
      // Keep the default error message when the response is not JSON.
    }

    throw new Error(errorMessage)
  }

  return response.json()
}