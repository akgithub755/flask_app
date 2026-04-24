<div class="loading-overlay">
    <div class="spinner">
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
        <div class="spinner-ring"></div>
    </div>
</div>

<style>
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(248, 250, 252, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        backdrop-filter: blur(4px);
    }

    .spinner {
        position: relative;
        width: 64px;
        height: 64px;
    }

    .spinner-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 4px solid transparent;
        animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }

    .spinner-ring:nth-child(1) {
        border-top-color: #03acba;
        animation-delay: -0.45s;
    }

    .spinner-ring:nth-child(2) {
        border-top-color: #0891b2;
        animation-delay: -0.3s;
    }

    .spinner-ring:nth-child(3) {
        border-top-color: #334155;
        animation-delay: -0.15s;
    }

    @keyframes spin {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>