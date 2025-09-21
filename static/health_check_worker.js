self.onmessage = function(event) {
    // Example: event.data could contain a URL to check
    const url = event.data.url;
    const uuid = event.data.uuid;
    let polling = true;
    self.postMessage({ log: "Starting health check worker for download from the worker uuid: " + uuid });

    async function poll() {
        while (polling) {
            try {
                const response = await fetch(`${url}`);
                if (response.ok) {
                    const data = await response.json();
                    if (data.status == "pending"){
                        // Handle pending status
                        self.postMessage({
                            status: 'pending',
                            code: response.status,
                            alert: false
                        });
                        self.postMessage({ log: "Pending on download uuid: " + uuid + " ..." });
                        // Wait before next poll
                    } else if (data.status == "completed"){
                        self.postMessage({
                            status: 'completed',
                            code: response.status,
                            alert: true
                        });
                        polling = false;
                        self.postMessage({ log: "Download completed for uuid: " + uuid });
                    } else if (typeof data.status === "string" && data.status.startsWith("failed")){
                        self.postMessage({
                            status: 'failed',
                            code: response.status,
                            alert: true
                        });
                        polling = false;
                        self.postMessage({ log: "Download failed for uuid: " + uuid });
                    }
                    
                } else {
                    self.postMessage({
                        status: 'unhealthy',
                        code: response.status,
                        alert: true
                    });
                    polling = false;
                }
            } catch (error) {
                self.postMessage({
                    status: 'error',
                    message: error.message,
                    alert: true
                });
                polling = false;
            }
            if (polling) {
                await new Promise(resolve => setTimeout(resolve, 2000)); // Poll every 2 seconds
            }
        }
    }

    poll();
};