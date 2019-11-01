using Microsoft.EntityFrameworkCore.Migrations;

namespace VCAuthn.Migrations
{
    public partial class UpdateAuthSession : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "ProofRequest",
                table: "Sessions",
                newName: "PresentationRequest");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "PresentationRequest",
                table: "Sessions",
                newName: "ProofRequest");
        }
    }
}
