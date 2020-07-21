using System;

namespace VCAuthn.Models
{
    [AttributeUsage(AttributeTargets.Property,
                Inherited = false,
                AllowMultiple = false)]
    internal sealed class OptionalAttribute : Attribute
    {
    }
}
