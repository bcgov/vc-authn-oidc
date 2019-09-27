using System;
using System.Threading.Tasks;
using VCAuthn.Migrations;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;

namespace VCAuthn.UrlShortener
{
    public class UrlShortenerService : IUrlShortenerService
    {
        private readonly StorageDbContext _context;
        private readonly string _baseUrl;

        public UrlShortenerService(StorageDbContext context, string baseUrl)
        {
            _context = context;
            _baseUrl = baseUrl;
        }

        /// <inheritdoc />
        public string CreateShortUrl(string url)
        {
            var key = Guid.NewGuid().ToString();

            if (AddUrl(key, url))
                return $"{_baseUrl}/{key}";

            return null;
        }

        /// <inheritdoc />
        public async Task<string> CreateShortUrlAsync(string url)
        {
            var key = Guid.NewGuid().ToString();

            if (await AddUrlAsync(key, url))
                return $"{_baseUrl}/{key}";

            return null;
        }

        /// <inheritdoc />
        public bool AddUrl(string key, string url)
        {
            _context.Add(new MappedUrl()
            {
                Key = key,
                Url = url
            });

            return _context.SaveChanges() == 1;
        }

        /// <inheritdoc />
        public async Task<bool> AddUrlAsync(string key, string url)
        {
            _context.Add(new MappedUrl()
            {
                Key = key,
                Url = url
            });

            return (await _context.SaveChangesAsync()) == 1;
        }

        /// <inheritdoc />
        public string GetUrl(string key)
        {
            var url = _context.MappedUrls.Find(key);
            return url?.Url;
        }

        /// <inheritdoc />
        public async Task<string> GetUrlAsync(string key)
        {
            var url = await _context.MappedUrls.FindAsync(key);
            return url?.Url;
        }

        /// <inheritdoc />
        public bool DeleteUrl(string key)
        {
            var url = _context.MappedUrls.Find(key);

            if (url == null)
                return false;

            _context.MappedUrls.Remove(url);
            return _context.SaveChanges() == 1;
        }

        /// <inheritdoc />
        public async Task<bool> DeleteUrlAsync(string key)
        {
            var url = await _context.MappedUrls.FindAsync(key);

            if (url == null)
                return false;

            _context.MappedUrls.Remove(url);
            return _context.SaveChanges() == 1;
        }
    }
}