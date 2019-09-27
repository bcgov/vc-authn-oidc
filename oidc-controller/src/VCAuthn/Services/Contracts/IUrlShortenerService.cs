using System.Threading.Tasks;

namespace VCAuthn.Services.Contracts
{
    /// <summary>
    /// Url Shortener Service.
    /// </summary>
    public interface IUrlShortenerService
    {
        /// <summary>
        /// Creates a short url.
        /// </summary>
        /// <param name="url">Url to create a shortened equivalent of.</param>
        /// <returns>Shortened url.</returns>
        string CreateShortUrl(string url);

        /// <summary>
        /// Creates a short url async.
        /// </summary>
        /// <param name="url">Url to create a shortened equivalent of.</param>
        /// <returns>Async shortened url.</returns>
        Task<string> CreateShortUrlAsync(string url);

        /// <summary>
        /// Adds a url to the persistance with a specified key.
        /// </summary>
        /// <param name="key">Key to link the url to.</param>
        /// <param name="url">Url to store.</param>
        /// <returns>Boolean status indicating if the url was persisted.</returns>
        bool AddUrl(string key, string url);

        /// <summary>
        /// Adds a url to the persistance with a specified key async.
        /// </summary>
        /// <param name="key">Key to link the url to.</param>
        /// <param name="url">Url to store.</param>
        /// <returns>Async boolean status indicating if the url was persisted.</returns>
        Task<bool> AddUrlAsync(string key, string url);

        /// <summary>
        /// Deletes a url from persistance.
        /// </summary>
        /// <param name="key">Key the url is identified by.</param>
        /// <returns>Boolean status indicating if the deletion of the url was sucessful</returns>
        bool DeleteUrl(string key);

        /// <summary>
        /// Deletes a url from persistance async.
        /// </summary>
        /// <param name="key">Key the url is identified by.</param>
        /// <returns>Async boolean status indicating if the deletion of the url was sucessful</returns>
        Task<bool> DeleteUrlAsync(string key);

        /// <summary>
        /// Gets a url from persistance by its associated key.
        /// </summary>
        /// <param name="key">Key associated to the url.</param>
        /// <returns>The url.</returns>
        string GetUrl(string key);

        /// <summary>
        /// Gets a url from persistance by its associated key async.
        /// </summary>
        /// <param name="key">Key associated to the url.</param>
        /// <returns>Async the url.</returns>
        Task<string> GetUrlAsync(string key);
    }
}